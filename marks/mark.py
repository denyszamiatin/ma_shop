"""Module to precess rating of the products"""
import psycopg2
from errors import errors


def add(conn, id_user: int, id_product: int, mark: int) -> None:
    """
    Add mark to the database. Used by User
    :param conn: psycopg2.extensions.connection
    :param id_user: int
    :param id_product: int
    :param mark: int
    :return: None
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(f"""
                INSERT INTO mark (id_user, id_product, rating)
                VALUES ('{id_user}', '{id_product}', '{mark}')
                """)
            conn.commit()
        except psycopg2.DatabaseError:
            raise errors.StoreError


def get_average(conn, id_product: int) -> float:
    """
    Return average rating of the product with id = product_id
    :param conn: psycopg2.extensions.connection
    :param id_product: int
    :return: float
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""select avg(rating) FROM mark WHERE id_product = '{id_product}'""")
            avg = cursor.fetchone()[0]
        return avg
    except TypeError:
        raise errors.StoreError


def update(conn, id_user: int, id_product: int, new_mark: int) -> None:
    """
    Set new value to the mark
    :param conn: psycopg2.extensions.connection
    :param id_user: int
    :param id_product: int
    :param new_mark: int
    :return: None
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""
            update mark 
            set rating = {new_mark} 
            where id_user = '{id_user}' and id_product = '{id_product}'""")
        if cursor.rowcount:
            conn.commit()
        else:
            raise errors.StoreError


def delete(conn, id_user: int, id_product: int) -> None:
    """
    Delete mark
    :param conn: psycopg2.extensions.connection
    :param id_user: int
    :param id_product: int
    :return: None
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""
            delete from mark
            where id_user = '{id_user}' and id_product = '{id_product}'""")
        if cursor.rowcount:
            conn.commit()
        else:
            raise errors.StoreError
