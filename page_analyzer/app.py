from http import HTTPStatus
import logging
import os
from typing import Optional

import dotenv
from psycopg2.extras import DictRow
import flask
import requests

from page_analyzer import consts, database, sql, utils

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

logger.info("Running Flask project.")

app: flask.Flask = flask.Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")

db = database.Database(app.config.get("DATABASE_URL"))
manager = sql.Manager(db)

logger.info("The project is successfully run.")


@app.errorhandler(500)
def internal_server_error(e):
    """Displays custom Error 500 page."""
    logger.error(f"Internal server error: {e}")
    return (
        flask.render_template('errors/500.html'),
        HTTPStatus.INTERNAL_SERVER_ERROR
    )


@app.errorhandler(404)
def not_found_error(e):
    """Displays custom Error 500 page."""
    logger.error(f"Page not found: {e}")
    return flask.render_template('errors/404.html'), HTTPStatus.NOT_FOUND


@app.get("/")
def index() -> str:
    """Logic for generating the main page."""
    messages: list = flask.get_flashed_messages(with_categories=True)
    url: str = flask.request.args.get("url", "")

    logger.info("Rendering home page.")

    return flask.render_template(
        consts.Template.INDEX.value,
        url=url,
        messages=messages
    )


@app.get("/urls")
def urls() -> str:
    """Logic for generating the list of URLs."""
    with db.connect():
        entries: list[DictRow] = manager.get_entries()
        last_checks: list[DictRow] = manager.get_last_checks()

    merged_entries: list[dict] = utils.merge_entries(entries, last_checks)

    logger.info("Rendering URLs page.")

    return flask.render_template(
        consts.Template.URLS.value,
        entries=merged_entries,
    )


@app.get("/urls/<int:id>")
def detail(id: int) -> flask.Response | str:
    """Logic for generating the page of a specific URL."""
    messages: list = flask.get_flashed_messages(with_categories=True)

    with db.connect():
        entry: DictRow = manager.get_entry(id)
        checks: list[DictRow] = manager.get_checks(id)

    if entry:
        logger.info(f"Rendering entry with id {id} detail page")
        return flask.render_template(
            consts.Template.DETAIL.value,
            entry=entry,
            checks=checks,
            messages=messages,
        )

    logger.warning(f"Entry {id} does not exist. Redirecting to the home page.")
    flask.flash(consts.Message.DOESNT_EXIST.value, "danger")
    return flask.redirect(flask.url_for("index"))


@app.post("/urls")
def urls_post() -> str:
    """Logic for handling POST request from the add URL form."""
    url: str = flask.request.form.to_dict().get("url")

    if not utils.is_valid_url(url):
        logger.info(f"Received an invalid url: {url}. Redirecting to URLs list.")

        flask.flash(consts.Message.INVALID_URL.value, "danger")

        return flask.render_template(
            consts.Template.INDEX.value,
            url=url,
            messages=flask.get_flashed_messages(with_categories=True),
            redirect_to=flask.url_for("urls"),
        ), HTTPStatus.UNPROCESSABLE_ENTITY

    with db.connect():
        pure_url: str = utils.sanitize_url(url)
        search_result: Optional[DictRow] = manager.search_entry_by_url(pure_url)

        if search_result:
            logger.info("Requested entry exists. Redirecting to its page.")
            url_id: int = search_result.get("id", 0)
            flask.flash(consts.Message.ALREADY_EXISTS.value, "info")
            return flask.redirect(flask.url_for("detail", id=url_id))

        entry: Optional[DictRow] = manager.create_entry(pure_url)

    if entry:
        logger.info("Entry was successfully added. Redirecting to its page.")
        url_id: int = entry.get("id", 0)
        flask.flash(consts.Message.ADD_SUCCESS.value, "success")
        return flask.redirect(flask.url_for("detail", id=url_id))

    logger.warning("The addition failed. Redirecting to home page.")
    flask.flash(consts.Message.ADD_FAILURE.value, "danger")
    return flask.redirect(flask.url_for("index", url=url))


@app.post("/urls/<int:id>/checks")
def checks_post(id: int):
    """Logic for handling URL check."""
    with db.connect():
        entry: Optional[DictRow] = manager.search_entry_by_id(id)

        if entry:
            try:
                response: requests.Response = utils.get_response(entry)
                args: tuple[int, str, str, str] = utils.make_check(response)
                manager.create_check(id, args)
                flask.flash(consts.Message.CHECK_SUCCESS.value, "success")

            except requests.exceptions.RequestException as e:
                logger.warning(f"The check failed due to network problems: {e}")
                flask.flash(consts.Message.CHECK_FAILURE.value, "danger")

            except Exception as e:
                logger.error(f"Error: {e}.", exc_info=True)
                flask.abort(HTTPStatus.INTERNAL_SERVER_ERROR)

        else:
            logger.error(f"Entry with id {id} isn't found.")
            flask.abort(HTTPStatus.INTERNAL_SERVER_ERROR)

        logger.info("Check is succesfully finished. Redirecting to entry page.")
        return flask.redirect(flask.url_for("detail", id=id))


if __name__ == "__main__":
    app.run()
