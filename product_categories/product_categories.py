"""category CRUD realisation"""

import psycopg2
from config import DATABASE


def create_category(conn, name: str) -> None:
    """
    Create new category
    conn: connection
    name: new category name
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute("insert into product_categories (name) values('{0}')".format(name))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            raise KeyError

def read_category(conn, id: int) -> str:
    """
    Read category from DB
    conn: connection
    id: category id in DB
    """
    with conn.cursor() as cursor:
        cursor.execute("select name from product_categories where id = {0}".format(id))
        try:
            return cursor.fetchone()[0]
        except TypeError:
            raise KeyError

def update_category(conn, id: int, new_name: str) -> None:
    """
    Update category in DB
    conn: connection
    id: category id in DB
    new_name: category new name
    """
    with conn.cursor() as cursor:
        cursor.execute("select name from product_categories where id = {0}".format(id))
        if cursor.fetchone():
            cursor.execute("update product_categories set name = '{0}' where id = {1}".format(new_name, id))
            conn.commit()
        else:
            raise KeyError

def delete_category(conn, id: int) -> None:
    """
    Delete category from DB
    conn: connection
    id: category id in DB
    """
    with conn.cursor() as cursor:
        cursor.execute("select name from product_categories where id = {0}".format(id))
        if cursor.fetchone():
            cursor.execute("delete from product_categories where id = {0}".format(id))
            conn.commit()
        else:
            raise KeyError
