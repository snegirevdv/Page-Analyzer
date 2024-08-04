import psycopg2


class Database:
    def __init__(self, database_url):
        self.database_url = database_url
        self.connection = None

    def connect(self):
        if self.is_connected:
            self.connection.close()

        self.connection = psycopg2.connect(self.database_url)
        self.connection.autocommit = True

        return self.connection

    def close(self):
        if self.is_connected:
            self.connection.close()

    def get_connection(self):
        if not self.is_connected:
            self.connect()
        return self.connection

    @property
    def is_connected(self):
        return self.connection and not self.connection.closed
