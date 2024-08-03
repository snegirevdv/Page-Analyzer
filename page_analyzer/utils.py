from typing import Optional
from urllib import parse

import bs4
import requests
from psycopg2.extras import DictRow
from validators.url import url

from page_analyzer import consts


def is_valid_url(original_url: str) -> bool:
    """Validates the URL."""
    return bool(url(original_url, simple_host=True))


def sanitize_url(url: str) -> str:
    """Cleans the URL from unnecessary elements."""
    parsed_url: parse.ParseResult = parse.urlparse(url)

    return parse.urlunparse(
        (parsed_url.scheme, parsed_url.netloc, "", "", "", "")
    )


def get_response(entry: DictRow) -> requests.Response:
    """Returns response for the url from the current entry."""
    url: str = entry.get("name", "")
    response: requests.Response = requests.get(url)
    response.raise_for_status()
    return response


def make_check(response: requests.Response) -> tuple[int, str, str, str]:
    """Performs a URL check and returns a tuple with the results."""
    parser = bs4.BeautifulSoup(response.content, "html.parser")

    status_code: int = response.status_code

    title_tag: Optional[bs4.Tag] = parser.find("title")
    title: str = title_tag.text[:consts.MAX_LENGTH] if title_tag else ""

    h1_tag: Optional[bs4.Tag] = parser.find("h1")
    h1: str = h1_tag.text[:consts.MAX_LENGTH] if h1_tag else ""

    description_tag: Optional[bs4.Tag] = parser.find(
        name="meta",
        attrs={"name": "description"},
    )
    description: str = (
        description_tag.get("content", "")[:consts.MAX_LENGTH]
        if description_tag else ""
    )

    return (status_code, title, h1, description)
