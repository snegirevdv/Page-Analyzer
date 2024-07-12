from datetime import datetime
import os
from urllib import parse

from bs4 import BeautifulSoup
import dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
import requests
from page_analyzer import consts, sql
from page_analyzer.database import Database
from validators.url import url as validate_url

dotenv.load_dotenv()

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.get("/")
def index() -> str:
    messages: list = get_flashed_messages(with_categories=True)
    url: str = request.args.get("url", "")

    return render_template(
        consts.INDEX_TEMPLATE,
        url=url,
        messages=messages
    )


@app.get("/urls")
def urls() -> str:
    with Database() as db:
        db.execute_query(sql.URLS)
        entries = db.cursor.fetchall()

    return render_template(
        consts.URLS_TEMPLATE,
        entries=entries
    )


@app.get("/urls/<int:id>")
def detail(id: int):
    messages: list = get_flashed_messages(with_categories=True)

    with Database() as db:
        db.execute_query(sql.DETAIL, id)
        entry = db.cursor.fetchone()
        db.execute_query(sql.CHECKS, id)
        checks = db.cursor.fetchall()

    if entry:
        return render_template(
            consts.DETAIL_TEMPLATE,
            entry=entry,
            checks=checks,
            messages=messages,
        )

    flash(consts.DOESNT_EXIST, consts.DANGER)
    return redirect(url_for('index'))


@app.post("/urls")
def urls_post():
    url = request.form.to_dict()["url"]

    if validate_url(url, simple_host=True) is not True:
        flash(consts.INVALID_URL, consts.DANGER)
        return render_template(
            consts.INDEX_TEMPLATE,
            url=url,
            messages=get_flashed_messages(with_categories=True),
            redirect_to=url_for('urls')
        ), 422

    parsed_url = parse.urlparse(url)

    pure_url = parse.urlunparse(
        (parsed_url.scheme, parsed_url.netloc, '', '', '', '')
    )

    with Database() as db:
        db.execute_query(sql.FIND_ID, pure_url)
        search_result = db.cursor.fetchone()

    if search_result:
        url_id = search_result["id"]
        flash(consts.ALREADY_EXISTS, consts.INFO)
        return redirect(url_for('detail', id=url_id))

    with Database() as db:
        db.execute_query(sql.NEW_ENTRY, pure_url, datetime.now())
        entry = db.cursor.fetchone()

    if entry:
        url_id = entry["id"]
        flash(consts.ADD_SUCCESS, consts.SUCCESS)
        return redirect(url_for('detail', id=url_id))

    flash(consts.ADD_FAILURE, consts.DANGER)
    return redirect(url_for('index', url=url))


@app.post('/urls/<int:id>/checks')
def checks_post(id):
    with Database() as db:
        db.execute_query(sql.FIND_URL, id)

        if entry := db.cursor.fetchone():
            try:
                url = entry["name"]
                response = requests.get(url)
                response.raise_for_status()
                status_code = response.status_code

                parser = BeautifulSoup(response.content, 'html.parser')

                title_tag = parser.find('title')
                title = title_tag.text if title_tag else ''

                h1_tag = parser.find('h1')
                h1 = h1_tag.text if h1_tag else ''

                description_tag = parser.find(
                    'meta',
                    attrs={'name': 'description'}
                )
                description = (
                    description_tag.get('content', '')
                    if description_tag
                    else ''
                )

                db.execute_query(
                    sql.NEW_CHECK,
                    id,
                    datetime.now(),
                    status_code,
                    title,
                    h1,
                    description,
                )

                flash(consts.CHECK_SUCCESS, consts.SUCCESS)

            except (
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
            ):
                flash(consts.CHECK_FAILURE, consts.DANGER)

            except db.exceptions:
                flash(consts.DB_ERROR, consts.DANGER)

        else:
            flash(consts.DB_ERROR, consts.DANGER)

    return redirect(url_for('detail', id=id))


if __name__ == "__main__":
    app.run()
