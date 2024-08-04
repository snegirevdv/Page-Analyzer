from datetime import datetime
from typing import Optional

from psycopg2.extras import DictCursor, DictRow

from page_analyzer.database import Database


class Manager:
    def __init__(self, db: Database):
        self.db = db
        self.cursor = None

    def create_cursor(self):
        self.cursor = self.db.get_connection().cursor(cursor_factory=DictCursor)
        return self.cursor

    def get_entries(self) -> list[DictRow]:
        sql = "SELECT id, name, created_at FROM urls;"
        with self.create_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

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
        with self.create_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_entry(self, id: int) -> Optional[DictRow]:
        """Returns an entry by id."""
        sql = "SELECT id, name, created_at FROM urls WHERE id = %s;"
        with self.create_cursor() as cursor:
            cursor.execute(sql, (id, ))
            return cursor.fetchone()

    def get_checks(self, id: int) -> list[DictRow]:
        """Returns a list of checks by id."""
        sql = """
            SELECT id, created_at, status_code, h1, title, description
            FROM url_checks
            WHERE url_id = %s
            ORDER BY id;
            """
        with self.create_cursor() as cursor:
            cursor.execute(sql, (id, ))
            return cursor.fetchall()

    def search_entry_by_url(self, url: str) -> Optional[DictRow]:
        """Finds an entry by URL."""
        sql = "SELECT id FROM urls WHERE name = %s LIMIT 1;"
        with self.create_cursor() as cursor:
            cursor.execute(sql, (url, ))
            return cursor.fetchone()

    def search_entry_by_id(self, id: int) -> Optional[DictRow]:
        """Finds an entry by id."""
        sql = "SELECT name FROM urls WHERE id = %s LIMIT 1;"
        with self.create_cursor() as cursor:
            cursor.execute(sql, (id, ))
            return cursor.fetchone()

    def create_entry(self, url: str) -> Optional[DictRow]:
        """Creates an entry."""
        sql = """
            INSERT INTO urls (name, created_at)
            VALUES (%s, %s) RETURNING id;
            """
        with self.create_cursor() as cursor:
            cursor.execute(sql, (url, datetime.now()))
            return cursor.fetchone()

    def create_check(self, id: int, args: tuple[int, str, str, str]):
        """Creates a check."""
        sql = """
            INSERT INTO url_checks
            (url_id, created_at, status_code, title, h1, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """
        with self.create_cursor() as cursor:
            cursor.execute(sql, (id, datetime.now(), *args))
