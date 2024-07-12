from datetime import datetime
from typing import Optional

from psycopg2.extras import DictRow

from page_analyzer import sql
from page_analyzer.database import Database


class DatabaseManager:
    """Manager for retrieving information and working with the database."""

    def get_entries(self) -> list[DictRow]:
        """Returns a list of entries."""
        with Database() as db:
            db.execute_query(sql.URLS)
            return db.cursor.fetchall()

    def get_entry(self, id: int) -> Optional[DictRow]:
        """Returns an entry by id."""
        with Database() as db:
            db.execute_query(sql.DETAIL, id)
            return db.cursor.fetchone()

    def get_checks(self, id: int) -> list[DictRow]:
        """Returns a list of checks by id."""
        with Database() as db:
            db.execute_query(sql.CHECKS, id)
            return db.cursor.fetchall()

    def search_entry_by_url(self, url: str) -> Optional[DictRow]:
        """Finds an entry by URL."""
        with Database() as db:
            db.execute_query(sql.FIND_ID, url)
            return db.cursor.fetchone()

    def search_entry_by_id(self, id: int) -> Optional[DictRow]:
        """Finds an entry by id."""
        with Database() as db:
            db.execute_query(sql.FIND_URL, id)
            return db.cursor.fetchone()

    def create_entry(self, url: str) -> Optional[DictRow]:
        """Creates an entry."""
        with Database() as db:
            db.execute_query(sql.NEW_ENTRY, url, datetime.now())
            return db.cursor.fetchone()

    def create_check(self, id: int, args: tuple[int, str, str, str]):
        """Creates a check."""
        with Database() as db:
            db.execute_query(sql.NEW_CHECK, id, datetime.now(), *args)
