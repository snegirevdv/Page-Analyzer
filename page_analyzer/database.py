import os
from pathlib import Path
from typing import Any

import dotenv
import psycopg2
from psycopg2.extras import DictCursor

dotenv.load_dotenv()


class Database:
    """Database query handler."""
    def __enter__(self) -> "Database":
        self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)

        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any):
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()

        self.cursor.close()
        self.connection.close()

    def execute_query(self, query_text: str, *args):
        """
        Executes a database query from a string.
        Accepts the query text and an unlimited number of parameters.
        """
        if args:
            self.cursor.execute(query_text, args)
        else:
            self.cursor.execute(query_text)

    def execute_file(self, file_name: str):
        """
        Executes a database query from a file.
        Accepts the file path containing the query.
        """
        path = Path(file_name)

        with path.open() as file:
            query_text = file.read()
            self.execute_query(query_text)
