from enum import Enum

MIGRATION = "database.sql"
MAX_LENGTH = 255


class Template(Enum):
    """Template URLs."""

    INDEX = "index.html"
    URLS = "urls.html"
    DETAIL = "detail.html"


class Message(Enum):
    """Flash message texts."""

    INVALID_URL = "Некорректный URL"
    ALREADY_EXISTS = "Страница уже существует"
    ADD_SUCCESS = "Страница успешно добавлена"
    ADD_FAILURE = "Ошибка при добавлении страницы"
    DOESNT_EXIST = "Такой страницы не существует"
    CHECK_SUCCESS = "Страница успешно проверена"
    CHECK_FAILURE = "Произошла ошибка при проверке"
