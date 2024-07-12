import os

import dotenv
import psycopg2

from psycopg2.extras import DictCursor

dotenv.load_dotenv(".env.development")


class Database:
    exceptions = (psycopg2.DatabaseError, psycopg2.OperationalError)

    def __enter__(self):
        self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query_text, *args):
        if args:
            self.cursor.execute(query_text, args)
        else:
            self.cursor.execute(query_text)

    def execute_file(self, file_name):
        with open(file_name) as file:
            query_text = file.read()
            self.execute_query(query_text)
