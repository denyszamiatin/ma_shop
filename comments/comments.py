"""
Module Comments with add, get, edit and delete
"""

import psycopg2
from errors import errors


def add(con, id_product: int, id_user: int, body: str) -> None:
    """
    Add new comment in db.
    :param con: str
    :param id_product: int
    :param id_user: int
    :param body: str
    :return: None
    """
    with con.cursor() as cursor:
        try:
            cursor.execute(f"""insert into Comments(id_product, id_user, body)
                                    values ({id_product}, {id_user}, {body})""")
            con.commit()
        except psycopg2.DatabaseError:
            raise errors.StoreError


def get(con, id_product: int) -> list:
    """
    Get comments from db using index parameter.
    :param con: str
    :param id_product: int
    :return: list
    """
    with con.cursor() as cursor:
        cursor.execute(f"""select id_user, body, date from Comments where id_product={id_product}""")
        try:
            result = cursor.fetchall()
        except TypeError:
            raise errors.StoreError
    return result


def edit(con, id: int, body: str) -> None:
    """
    Update comment in db.
    :param con: str
    :param id: int
    :param body: str
    :return: None
    """
    with con.cursor() as cursor:
        cursor.execute(f"""update Comments set body={body} where id={id}""")
        if cursor.rowcount:
            con.commit()
        else:
            raise errors.StoreError


def delete(con, id: int) -> None:
    """
    Delete comment in db.
    :param con: str
    :param id: int
    :return: None
    """
    with con.cursor() as cursor:
        cursor.execute(f"""delete from Comments where id={id}""")
        if cursor.rowcount:
            con.commit()
        else:
            raise errors.StoreError
