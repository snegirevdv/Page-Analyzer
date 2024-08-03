import os
from typing import Optional

import dotenv
from psycopg2.extras import DictRow
import flask
import requests

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
        consts.Template.INDEX.value,
        url=url,
        messages=messages
    )


@app.get("/urls")
def urls() -> str:
    """Logic for generating the list of URLs."""
    entries: list[DictRow] = db_manager.get_entries()

    return flask.render_template(
        consts.Template.URLS.value,
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
            consts.Template.DETAIL.value,
            entry=entry,
            checks=checks,
            messages=messages,
        )

    flask.flash(consts.Message.DOESNT_EXIST.value, "danger")
    return flask.redirect(flask.url_for("index"))


@app.post("/urls")
def urls_post() -> str:
    """Logic for handling POST request from the add URL form."""
    url: str = flask.request.form.to_dict().get("url")

    if not utils.is_valid_url(url):
        flask.flash(consts.Message.INVALID_URL.value, "danger")

        return flask.render_template(
            consts.Template.INDEX.value,
            url=url,
            messages=flask.get_flashed_messages(with_categories=True),
            redirect_to=flask.url_for("urls"),
        ), 422

    pure_url: str = utils.sanitize_url(url)
    search_result: Optional[DictRow] = db_manager.search_entry_by_url(pure_url)

    if search_result:
        url_id: int = search_result.get("id", 0)
        flask.flash(consts.Message.ALREADY_EXISTS.value, "info")
        return flask.redirect(flask.url_for("detail", id=url_id))

    entry: Optional[DictRow] = db_manager.create_entry(pure_url)

    if entry:
        url_id: int = entry.get("id", 0)
        flask.flash(consts.Message.ADD_SUCCESS.value, "success")
        return flask.redirect(flask.url_for("detail", id=url_id))

    flask.flash(consts.Message.ADD_FAILURE.value, "danger")
    return flask.redirect(flask.url_for("index", url=url))


@app.post("/urls/<int:id>/checks")
def checks_post(id: int):
    """Logic for handling URL check."""
    entry: Optional[DictRow] = db_manager.search_entry_by_id(id)

    if entry:
        try:
            response: requests.Response = utils.get_response(entry)
            args: tuple[int, str, str, str] = utils.make_check(response)
            db_manager.create_check(id, args)
            flask.flash(consts.Message.CHECK_SUCCESS.value, "success")

        except consts.Error.REQUEST:
            flask.flash(consts.Message.CHECK_FAILURE.value, "danger")

        except consts.Error.DATABASE:
            flask.flash(consts.Message.DB_ERROR, "danger")

    else:
        flask.flash(consts.Message.DB_ERROR, "danger")

    return flask.redirect(flask.url_for("detail", id=id))


if __name__ == "__main__":
    app.run()
