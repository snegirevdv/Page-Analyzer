import logging
import psycopg2

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
                logger.debug("Closing existing database connection.")
                self.connection.close()

            logger.info("Connecting to the database.")
            self.connection = psycopg2.connect(self.__database_url)
            self.connection.autocommit = True
            logger.info("Successfully connected to the database.")

            return self.connection

        except Exception as e:
            logger.error("Failed to connect to the database.", exc_info=True)
            raise e

    def close(self):
        """Closes the connection if it exists."""
        if self.is_connected:
            logger.info("Closing the database connection.")
            self.connection.close()
        logger.debug("No database connections to close.")

    def get_connection(self):
        """Creates a connection if it doesn't exists and returns it"""
        if not self.is_connected:
            logger.debug("No database connections. Starting a new connection.")
            self.connect()
        return self.connection

    @property
    def is_connected(self) -> bool:
        """Checks if the connection exists and isn't closed."""
        return self.connection and not self.connection.closed
