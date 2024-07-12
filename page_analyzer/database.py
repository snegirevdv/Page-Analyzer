import os
from typing import Any, Self

import dotenv
import psycopg2
from psycopg2.extras import DictCursor

dotenv.load_dotenv()


class Database:
    """Обработчик запросов к базе данных."""
    def __enter__(self) -> Self:
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
        Выполняет запрос к базе данных из строки.
        Принимает текст запроса и неограниченное количество параметров.
        """
        if args:
            self.cursor.execute(query_text, args)
        else:
            self.cursor.execute(query_text)

    def execute_file(self, file_name: str):
        """
        Выполняет запрос к базе данных из файла.
        Принимает адрес файла, содержащего запрос.
        """
        with open(file_name) as file:
            query_text = file.read()
            self.execute_query(query_text)
