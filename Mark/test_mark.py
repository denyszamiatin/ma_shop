import pytest
import sqlite3
import mark


def tests_add_mark():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE mark (
            id_user INTEGER,
            id_product INTEGER,
            mark_date DATE,
            rating INTEGER
        )""")

    mark.add_mark(cursor, 2, 5, 2)
    mark.add_mark(cursor, 2, 5, 4)
    assert mark.average_rating(cursor, 5) == 3
