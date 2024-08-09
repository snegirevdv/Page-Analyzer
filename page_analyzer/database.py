import logging
import psycopg2

from page_analyzer.exceptions import DatabaseConnectionError

logger = logging.getLogger(__name__)


class Database:
    """
    A class managing database connections using psycopg2.

    Attributes:
        connection: the connection object.
        is_connected: the current connection state.
    """

    def __init__(self, database_url: str):
        self.__database_url = database_url
        self.connection = None

    def connect(self):
        """Creates a connection to the database."""
        try:
            if self.is_connected:
                self.connection.close()

            self.connection = psycopg2.connect(self.__database_url)
            self.connection.autocommit = True

            return self.connection

        except psycopg2.Error as e:
            logger.error(f"Connection error: {e}", exc_info=True)
            raise DatabaseConnectionError

    def close(self):
        """Closes the connection if it exists."""
        self.connection.close()

    def get_connection(self):
        """Creates a connection if it doesn't exists and returns it"""
        if not self.is_connected:
            self.connect()
        return self.connection

    @property
    def is_connected(self) -> bool:
        """Checks if the connection exists and isn't closed."""
        return self.connection and not self.connection.closed
