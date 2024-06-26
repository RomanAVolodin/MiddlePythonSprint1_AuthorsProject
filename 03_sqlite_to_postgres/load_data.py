import os
import sqlite3
from contextlib import closing

import psycopg
from dotenv import load_dotenv
from psycopg import connection as _connection
from psycopg import sql
from psycopg.rows import dict_row

from loaders import PostgresSaver, SQLiteLoader
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

load_dotenv()

DSL = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('SQL_HOST'),
    'port': os.getenv('SQL_PORT'),
}

TABLES = {
    FilmWork: 'film_work',
    Person: 'person',
    Genre: 'genre',
    PersonFilmWork: 'person_film_work',
    GenreFilmWork: 'genre_film_work',
}


def load_from_sqlite(connection: sqlite3.Connection, conn: _connection) -> None:
    sqlite_loader = SQLiteLoader(connection)
    postgres_saver = PostgresSaver(conn)

    for klass, table in TABLES.items():
        sqlite_data = sqlite_loader.load_data(table)
        for batch in sqlite_data:
            data_to_load = [klass.get_values(item) for item in batch]
            query = sql.SQL(
                'INSERT INTO content.{table} ({table_fields}) VALUES ({values}) ON CONFLICT (id) DO NOTHING'
            ).format(
                table=sql.Identifier(table),
                table_fields=sql.SQL(',').join([sql.Identifier(field) for field in klass.model_fields]),
                values=sql.SQL(',').join(sql.Placeholder() * len(klass.model_fields)),
            )
            postgres_saver.save_data(query, data_to_load)


if __name__ == '__main__':
    with closing(sqlite3.connect('db.sqlite')) as sqlite_conn, closing(
        psycopg.connect(**DSL, row_factory=dict_row)
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

    print('🎉 Все данные перенесены 👍')
