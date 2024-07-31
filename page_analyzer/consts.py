import psycopg2
import requests

MIGRATION = "database.sql"

TEMPLATES = {
    "index": "index.html",
    "urls": "urls.html",
    "detail": "detail.html",
}

MESSAGES = {
    "invalid_url": "Некорректный URL",
    "already_exists": "Страница уже существует",
    "add_success": "Страница успешно добавлена",
    "add_failure": "Ошибка при добавлении страницы",
    "doesnt_exist": "Такой страницы не существует",
    "check_success": "Страница успешно проверена",
    "check_failure": "Произошла ошибка при проверке",
    "db_error": "Ошибка при обращении к базе данных",
}

REQUEST_ERRRORS = (
    requests.exceptions.HTTPError,
    requests.exceptions.ConnectionError,
)

DATABASE_ERRORS = (
    psycopg2.DatabaseError,
    psycopg2.OperationalError,
)

MAX_LENGTH = 255
