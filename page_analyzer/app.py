import os
from typing import Optional

import dotenv
from psycopg2.extras import DictRow
import flask

from page_analyzer import consts, manager, utils

dotenv.load_dotenv()

app: flask.Flask = flask.Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
db_manager: manager.DatabaseManager = manager.DatabaseManager()


@app.get("/")
def index() -> str:
    """Логика генерации главной страницы."""
    messages: list = flask.get_flashed_messages(with_categories=True)
    url: str = flask.request.args.get("url", "")

    return flask.render_template(
        consts.INDEX_TEMPLATE,
        url=url,
        messages=messages
    )


@app.get("/urls")
def urls() -> str:
    """Логика генерации списка URL."""
    entries: list[DictRow] = db_manager.get_entries()

    return flask.render_template(
        consts.URLS_TEMPLATE,
        entries=entries,
    )


@app.get("/urls/<int:id>")
def detail(id: int) -> flask.Response | str:
    """Логика генерации страницы отдельного URL."""
    messages: list = flask.get_flashed_messages(with_categories=True)
    entry: DictRow = db_manager.get_entry(id)
    checks: list[DictRow] = db_manager.get_checks(id)

    if entry:
        return flask.render_template(
            consts.DETAIL_TEMPLATE,
            entry=entry,
            checks=checks,
            messages=messages,
        )

    flask.flash(consts.DOESNT_EXIST, consts.DANGER)
    return flask.redirect(flask.url_for("index"))


@app.post("/urls")
def urls_post() -> str:
    """Логика обработки POST-запроса из формы добавления URL."""
    url: str = flask.request.form.to_dict().get("url")

    if not utils.validate_url(url):
        flask.flash(consts.INVALID_URL, consts.DANGER)

        return flask.render_template(
            consts.INDEX_TEMPLATE,
            url=url,
            messages=flask.get_flashed_messages(with_categories=True),
            redirect_to=flask.url_for("urls"),
        ), 422

    pure_url: str = utils.sanitize_url(url)
    search_result: Optional[DictRow] = db_manager.search_entry_by_url(pure_url)

    if search_result:
        url_id: int = search_result.get('id', 0)
        flask.flash(consts.ALREADY_EXISTS, consts.INFO)
        return flask.redirect(flask.url_for("detail", id=url_id))

    entry: Optional[DictRow] = db_manager.create_entry(pure_url)

    if entry:
        url_id: int = entry.get('id', 0)
        flask.flash(consts.ADD_SUCCESS, consts.SUCCESS)
        return flask.redirect(flask.url_for("detail", id=url_id))

    flask.flash(consts.ADD_FAILURE, consts.DANGER)
    return flask.redirect(flask.url_for("index", url=url))


@app.post('/urls/<int:id>/checks')
def checks_post(id: int):
    """Логика обработки проверки URL."""
    entry: Optional[DictRow] = db_manager.search_entry_by_id(id)

    if entry:
        try:
            args: tuple[int, str, str, str] = utils.make_check(entry)
            db_manager.create_check(id, args)
            flask.flash(consts.CHECK_SUCCESS, consts.SUCCESS)

        except consts.REQUEST_ERRRORS:
            flask.flash(consts.CHECK_FAILURE, consts.DANGER)

        except consts.DATABASE_ERRORS:
            flask.flash(consts.DB_ERROR, consts.DANGER)

    else:
        flask.flash(consts.DB_ERROR, consts.DANGER)

    return flask.redirect(flask.url_for("detail", id=id))


if __name__ == "__main__":
    app.run()
