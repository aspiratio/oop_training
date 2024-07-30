import sqlite3


class SQLiteConnectionManager:
    def __init__(self, dbname: str) -> None:
        self._dbname = dbname

    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(self._dbname)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.connection.close()
