from typing import Optional
from urllib import parse

import bs4
import requests
from psycopg2.extras import DictRow
from validators.url import url


def validate_url(original_url: str) -> bool:
    """Валидирует URL."""
    return bool(url(original_url, simple_host=True))


def sanitize_url(url: str) -> str:
    """Очищает URL от лишних элементов."""
    parsed_url: parse.ParseResult = parse.urlparse(url)

    return parse.urlunparse(
        (parsed_url.scheme, parsed_url.netloc, '', '', '', '')
    )


def make_check(entry: DictRow) -> tuple[int, str, str, str]:
    """Проводит проверку URL и возвращает кортеж с результатами проверки."""
    url: str = entry.get("name", "")

    response: requests.Response = requests.get(url)
    response.raise_for_status()
    parser = bs4.BeautifulSoup(response.content, "html.parser")

    status_code: int = response.status_code

    title_tag: Optional[bs4.Tag] = parser.find("title")
    title: str = title_tag.text if title_tag else ""

    h1_tag: Optional[bs4.Tag] = parser.find("h1")
    h1: str = h1_tag.text if h1_tag else ""

    description_tag: Optional[bs4.Tag] = parser.find(
        name="meta",
        attrs={"name": "description"},
    )
    description: str = (
        description_tag.get("content", "")
        if description_tag else ""
    )

    return (status_code, title, h1, description)
