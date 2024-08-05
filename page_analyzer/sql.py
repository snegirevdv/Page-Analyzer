from datetime import datetime
import logging

from psycopg2.extras import DictCursor, DictRow

from page_analyzer.database import Database

logger = logging.getLogger(__name__)


class Manager:
    def __init__(self, db: Database):
        self.db = db
        self.cursor = None

    def _create_cursor(self):
        """Returns a new dict cursor."""
        logger.info("Creating a connection cursor.")

        try:
            self.cursor = (self.db
                           .get_connection()
                           .cursor(cursor_factory=DictCursor))

        except Exception as e:
            logger.error(f"Connection error: {e}.", exc_info=True)
            raise

        return self.cursor

    def _execute(self, sql: str, *args, all: bool) -> DictRow | list[DictRow]:
        """
        Executes a query and returns the result.

        If param all is True, returns the list of entries,
        else returns a single entry.
        """
        logger.info(f"Executing a SQL query: {sql.format(*args)}")
        with self._create_cursor() as cursor:
            try:
                cursor.execute(sql, args)
                logger.info("The query is succesfully executed.")

                if all:
                    return cursor.fetchall()

                return cursor.fetchone()

            except Exception as e:
                logger.error(f"SQL error: {e}.", exc_info=True)

    def get_entries(self) -> list[DictRow]:
        """Returns a list of entries."""
        sql = "SELECT id, name, created_at FROM urls;"
        return self._execute(sql, all=True)

    def get_last_checks(self) -> list[DictRow]:
        """Returns a list of entries."""
        sql = """
            SELECT DISTINCT ON (url_id)
                url_id as id,
                created_at as last_check_date,
                status_code as last_check_status_code
            FROM url_checks
            ORDER BY url_id, created_at DESC;
            """
        return self._execute(sql, all=True)

    def get_entry(self, id: int) -> DictRow:
        """Returns an entry by id."""
        sql = "SELECT id, name, created_at FROM urls WHERE id = %s;"
        return self._execute(sql, id, all=False)

    def get_checks(self, id: int) -> list[DictRow]:
        """Returns a list of checks by id."""
        sql = """
            SELECT id, created_at, status_code, h1, title, description
            FROM url_checks
            WHERE url_id = %s
            ORDER BY id;
            """
        return self._execute(sql, id, all=True)

    def search_entry_by_url(self, url: str) -> DictRow:
        """Finds an entry by URL."""
        sql = "SELECT id FROM urls WHERE name = %s LIMIT 1;"
        return self._execute(sql, url, all=False)

    def search_entry_by_id(self, id: int) -> DictRow:
        """Finds an entry by id."""
        sql = "SELECT name FROM urls WHERE id = %s LIMIT 1;"
        return self._execute(sql, id, all=False)

    def create_entry(self, url: str) -> DictRow:
        """Creates an entry."""
        sql = """
            INSERT INTO urls (name, created_at)
            VALUES (%s, %s) RETURNING id;
            """
        return self._execute(sql, url, datetime.now(), all=False)

    def create_check(self, id: int, args: tuple[int, str, str, str]) -> DictRow:
        """Creates a check."""
        sql = """
            INSERT INTO url_checks
            (url_id, created_at, status_code, title, h1, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """
        return self._execute(sql, id, datetime.now(), *args, all=False)
