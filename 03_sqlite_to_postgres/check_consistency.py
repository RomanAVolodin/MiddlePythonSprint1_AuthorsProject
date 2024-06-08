import sqlite3
from contextlib import closing

import psycopg
from psycopg.rows import dict_row

from load_data import DSL, TABLES
from loaders import BATCH_SIZE


if __name__ == '__main__':
    with closing(sqlite3.connect('db.sqlite')) as sqlite_conn, closing(psycopg.connect(**DSL)) as pg_conn:
        sqlite_conn.row_factory = sqlite3.Row
        with closing(sqlite_conn.cursor()) as sqlite_cursor, closing(pg_conn.cursor(row_factory=dict_row)) as pg_cursor:
            for klass, table in TABLES.items():
                sqlite_cursor.execute(f'SELECT * FROM {table}  ORDER BY created_at DESC')
                while batch := sqlite_cursor.fetchmany(BATCH_SIZE):
                    originals = [klass(**dict(item)) for item in batch]
                    ids = [item.id for item in originals]
                    pg_cursor.execute(f'SELECT * FROM content.{table} WHERE id = ANY(%s) ORDER BY created DESC', [ids])

                    transferred_items = {}

                    for transferred_item in pg_cursor.fetchall():
                        transferred_items[transferred_item['id']] = transferred_item

                    for original in originals:
                        assert original.id in transferred_items
                        transferred_item = transferred_items[original.id]
                        transferred_item['created_at'] = str(transferred_item.pop('created'))
                        transferred_item['updated_at'] = str(transferred_item.pop('modified', None))
                        transferred_item = klass(**transferred_item)

                        original.created = original.created.replace(tzinfo=None)
                        if hasattr(original, 'modified'):
                            original.modified = original.modified.replace(tzinfo=None)

                        assert original == transferred_item

    print('🎉 Все данные успешно перенесены 👍')
