import sqlite3
from contextlib import closing
from typing import Generator

from psycopg import connection as _connection
from psycopg import sql

BATCH_SIZE = 100


class SQLiteLoader:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.row_factory = sqlite3.Row

    def load_data(self, table: str) -> Generator[list[sqlite3.Row], None, None]:
        query = f'SELECT * FROM {table}'
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(query)
            while results := cursor.fetchmany(BATCH_SIZE):
                yield results


class PostgresSaver:
    def __init__(self, conn: _connection) -> None:
        self.conn = conn

    def save_data(self, query: sql.Composed, data: list) -> None:
        with closing(self.conn.cursor()) as cursor:
            cursor.executemany(query, data)
            self.conn.commit()
