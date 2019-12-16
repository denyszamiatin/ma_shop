"""category CRUD realisation"""

import psycopg2
import errors.errors as errors

def create(conn, name: str) -> None:
    """
    Create new category
    conn: connection
    name: new category name
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(f"insert into product_categories (name) values('{name}')")
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            raise errors.StoreError


def read(conn, category_id: int) -> str:
    """
    Read category from DB
    conn: connection
    id: category id in DB
    """
    with conn.cursor() as cursor:
        cursor.execute(f"select name from product_categories where id = {category_id}")
        try:
            return cursor.fetchone()[0]
        except TypeError:
            raise errors.StoreError


def update(conn, category_id: int, new_name: str) -> None:
    """
    Update category in DB
    conn: connection
    id: category id in DB
    new_name: category new name
    """
    with conn.cursor() as cursor:
        cursor.execute(f"select name from product_categories where id = {category_id}")
        if cursor.fetchone():
            cursor.execute(f"update product_categories set name = '{new_name}' where id = {category_id}")
            conn.commit()
        else:
            raise errors.StoreError


def delete(conn, category_id: int) -> None:
    """
    Delete category from DB
    conn: connection
    id: category id in DB
    """
    with conn.cursor() as cursor:
        cursor.execute(f"delete from product_categories where id = {category_id} returning id")
        if cursor.fetchone():
            conn.commit()
        else:
            raise errors.StoreError
