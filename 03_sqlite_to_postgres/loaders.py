import sqlite3
from typing import Generator

from psycopg import connection as _connection
from psycopg import sql

from logger import logger

BATCH_SIZE = 100


class SQLiteLoader:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        self.curs = conn.cursor()

    def load_data(self, table: str) -> Generator[list[sqlite3.Row], None, None]:
        query = f'SELECT * FROM {table}'
        try:
            self.curs.execute(query)
        except Exception as error:
            logger.error('Ошибка выгрузки данных из таблицы %s: %s', table, error)
        while results := self.curs.fetchmany(BATCH_SIZE):
            yield results


class PostgresSaver:
    def __init__(self, conn: _connection) -> None:
        self.conn = conn
        self.curs = conn.cursor()

    def save_data(self, query: sql.Composed, data: list) -> None:
        try:
            self.curs.executemany(query, data)
        except Exception as error:
            logger.error('Ошибка загрузки данных: %s', error)
        else:
            self.conn.commit()
