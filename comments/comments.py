"""
Module Comments with add, get, edit and delete
"""


import psycopg2
import errors.errors


def add(con, product_id: int, user_id: int, body: str) -> None:
    """
    Add new comment in db.
    :param con: str
    :param product_id: int
    :param user_id: int
    :param body: str
    :return: None
    """
    with con.cursor() as cursor:
        try:
            cursor.execute(f"""INSERT INTO Comments(product_id, user_id, body)
                                    VALUES ({product_id}, {user_id}, {body})"""
            con.commit()
        except psycopg2.DatabaseError:
            raise errors.errors.StoreError


def get(con, product_id: int) -> list:
    """
    Get comments from db using index parameter.
    :param con: str
    :param product_id: int
    :return: list
    """
    with con.cursor() as cursor:
        cursor.execute(f"""SELECT user_id, body, date FROM Comments WHERE product_id={product_id}""")
        try:
            result = cursor.fetchall()
        except TypeError:
            raise errors.errors.StoreError
    return result


def edit(con, comment_id: int, body: str) -> None:
    """
    Update comment in db.
    :param con: str
    :param comment_id: int
    :param body: str
    :return: None
    """
    with con.cursor() as cursor:
        try:
            cursor.execute(f"""UPDATE Comments SET body={body} WHERE comment_id={comment_id}""")
            con.commit()
        except TypeError:
            raise errors.errors.StoreError


def delete(con, comment_id: int) -> None:
    """
    Delete comment in db.
    :param con: str
    :param comment_id: int
    :return: None
    """
    with con.cursor() as cursor:
        try:
            cursor.execute(f"""DELETE FROM Comments WHERE comments_id={comment_id}""")
            con.commit()
        except TypeError:
            raise errors.errors.StoreError
