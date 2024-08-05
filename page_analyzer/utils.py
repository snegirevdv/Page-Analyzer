from collections import defaultdict
import logging
from typing import Optional
from urllib import parse

import bs4
import requests
from psycopg2.extras import DictRow
from validators.url import url

from page_analyzer import consts

logger = logging.getLogger(__name__)


def merge_entries(entries: list[DictRow], checks: list[DictRow]) -> list[dict]:
    """Returns a list of entries merged with the check list."""
    result = defaultdict(dict)

    for entry in entries:
        result[entry["id"]].update(entry)

    for check in checks:
        result[check["id"]].update(check)

    return [result[key] for key in sorted(result, reverse=True)]


def is_valid_url(original_url: str) -> bool:
    """Validates the URL."""
    return bool(url(original_url, simple_host=True))


def sanitize_url(url: str) -> str:
    """Cleans the URL from unnecessary elements."""
    logger.info("URL normalizing started.")

    try:
        parsed_url: parse.ParseResult = parse.urlparse(url)
        sanitized_url: str = parse.urlunparse(
            (parsed_url.scheme, parsed_url.netloc, "", "", "", ""),
        )

    except Exception as e:
        logger.error(f"URL normalizing failed. Error: {e}", exc_info=True)
        raise

    logger.info("URL succesfully normalized.")
    return sanitized_url


def get_response(entry: DictRow) -> requests.Response:
    """Returns response for the url from the current entry."""
    url: str = entry.get("name", "")
    logger.info("Receiving HTTP response started.")

    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()

    except Exception as e:
        logger.error(f"HTTP error: {e}", exc_info=True)
        raise

    logger.info("HTTP response successfully received.")
    return response


def make_check(response: requests.Response) -> tuple[int, str, str, str]:
    """Performs a URL check and returns a tuple with the results."""
    logger.info("Creating a parser.")
    parser = bs4.BeautifulSoup(response.content, "html.parser")
    logger.info("Parsing is started.")

    try:
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

    except Exception as e:
        logger.error(f"Parsing error: {e}", exc_info=True)
        raise

    logger.info("Parsing was succesfully finished.")
    return (status_code, title, h1, description)
