class DatabaseConnectionError(BaseException):
    """Error while connecting to database."""


class SqlError(BaseException):
    """Error while executing queries"""


class ParsingError(BaseException):
    """Error while data parsing."""


class ResponseError(BaseException):
    """Error while performing HTTP requests"""
