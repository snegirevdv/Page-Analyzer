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
    """Logic for generating the main page."""
    messages: list = flask.get_flashed_messages(with_categories=True)
    url: str = flask.request.args.get("url", "")

    return flask.render_template(
        consts.TEMPLATES["index"],
        url=url,
        messages=messages
    )


@app.get("/urls")
def urls() -> str:
    """Logic for generating the list of URLs."""
    entries: list[DictRow] = db_manager.get_entries()

    return flask.render_template(
        consts.TEMPLATES["urls"],
        entries=entries,
    )


@app.get("/urls/<int:id>")
def detail(id: int) -> flask.Response | str:
    """Logic for generating the page of a specific URL."""
    messages: list = flask.get_flashed_messages(with_categories=True)
    entry: DictRow = db_manager.get_entry(id)
    checks: list[DictRow] = db_manager.get_checks(id)

    if entry:
        return flask.render_template(
            consts.TEMPLATES["detail"],
            entry=entry,
            checks=checks,
            messages=messages,
        )

    flask.flash(consts.MESSAGES["doesnt_exist"], "danger")
    return flask.redirect(flask.url_for("index"))


@app.post("/urls")
def urls_post() -> str:
    """Logic for handling POST request from the add URL form."""
    url: str = flask.request.form.to_dict().get("url")

    if not utils.validate_url(url):
        flask.flash(consts.MESSAGES["invalid_url"], "danger")

        return flask.render_template(
            consts.TEMPLATES["index"],
            url=url,
            messages=flask.get_flashed_messages(with_categories=True),
            redirect_to=flask.url_for("urls"),
        ), 422

    pure_url: str = utils.sanitize_url(url)
    search_result: Optional[DictRow] = db_manager.search_entry_by_url(pure_url)

    if search_result:
        url_id: int = search_result.get("id", 0)
        flask.flash(consts.MESSAGES["already_exists"], "info")
        return flask.redirect(flask.url_for("detail", id=url_id))

    entry: Optional[DictRow] = db_manager.create_entry(pure_url)

    if entry:
        url_id: int = entry.get("id", 0)
        flask.flash(consts.MESSAGES["add_success"], "success")
        return flask.redirect(flask.url_for("detail", id=url_id))

    flask.flash(consts.MESSAGES["add_failure"], "danger")
    return flask.redirect(flask.url_for("index", url=url))


@app.post("/urls/<int:id>/checks")
def checks_post(id: int):
    """Logic for handling URL check."""
    entry: Optional[DictRow] = db_manager.search_entry_by_id(id)

    if entry:
        try:
            args: tuple[int, str, str, str] = utils.make_check(entry)
            db_manager.create_check(id, args)
            flask.flash(consts.MESSAGES["check_success"], "success")

        except consts.REQUEST_ERRRORS:
            flask.flash(consts.MESSAGES["check_failure"], "danger")

        except consts.DATABASE_ERRORS:
            flask.flash(consts.MESSAGES["db_error"], "danger")

    else:
        flask.flash(consts.MESSAGES["db_error"], "danger")

    return flask.redirect(flask.url_for("detail", id=id))


if __name__ == "__main__":
    app.run()
