from enum import StrEnum
from typing import NamedTuple
import psycopg2
import requests

MIGRATION = "database.sql"
MAX_LENGTH = 255


class Template(StrEnum):
    """Template URLs."""

    INDEX = "index.html"
    URLS = "urls.html"
    DETAIL = "detail.html"


class Message(StrEnum):
    """Flash message texts."""

    INVALID_URL = "Некорректный URL"
    ALREADY_EXISTS = "Страница уже существует"
    ADD_SUCCESS = "Страница успешно добавлена"
    ADD_FAILURE = "Ошибка при добавлении страницы"
    DOESNT_EXIST = "Такой страницы не существует"
    CHECK_SUCCESS = "Страница успешно проверена"
    CHECK_FAILURE = "Произошла ошибка при проверке"
    DB_ERROR = "Ошибка при обращении к базе данных"


class Error(NamedTuple):
    """Exception type lists."""

    REQUEST = (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
    )

    DATABASE = (
        psycopg2.DatabaseError,
        psycopg2.OperationalError,
    )
