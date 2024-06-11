import sqlite3
from typing import Self


class SQLiteDBClient:
    def __init__(self, name: str):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()

    # Define context managers
    # These manage the lifecycle when used in "with" statements
    def __enter__(self: Self):
        return self

    # Automcatically close connection and cursor on exit
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):        
        if commit:
            self.commit()
        self.connection.close()

    def deserialise(self: Self, bytes: bytes):
        self.connection.deserialize(bytes)

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()