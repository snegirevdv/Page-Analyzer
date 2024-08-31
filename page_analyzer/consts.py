from enum import Enum

MAX_LENGTH = 255
LOGGER_SIZE = 1_000_000


class Template(Enum):
    """Template URLs."""

    INDEX = "index.html"
    URLS = "urls.html"
    DETAIL = "detail.html"


class Message(Enum):
    """Flash message texts."""

    INVALID_URL = "Invalid URL"
    ALREADY_EXISTS = "The website already exists"
    ADD_SUCCESS = "Website added successfully"
    ADD_FAILURE = "Error occurred while adding the website"
    DOESNT_EXIST = "The website does not exist"
    CHECK_SUCCESS = "Website checked successfully"
    CHECK_FAILURE = "Error occurred while checking the website"
