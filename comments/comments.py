"""
Module Comments with add, get, edit and delete
"""


from errors import errors


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
            cursor.execute(f"""insert into Comments(product_id, user_id, body)
                                    values ({product_id}, {user_id}, {body})""")
            con.commit()
        except psycopg2.DatabaseError:
            raise errors.StoreError


def get(con, product_id: int) -> list:
    """
    Get comments from db using index parameter.
    :param con: str
    :param product_id: int
    :return: list
    """
    with con.cursor() as cursor:
        cursor.execute(f"""select user_id, body, date from Comments where product_id={product_id}""")
        try:
            result = cursor.fetchall()
        except TypeError:
            raise errors.StoreError
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
        cursor.execute(f"""update Comments set body={body} where comment_id={comment_id}""")
        if cursor.rowcount:
            con.commit()
        else:
            raise errors.StoreError


def delete(con, comment_id: int) -> None:
    """
    Delete comment in db.
    :param con: str
    :param comment_id: int
    :return: None
    """
    with con.cursor() as cursor:
        cursor.execute(f"""delete from Comments where comments_id={comment_id}""")
        if cursor.rowcount:
            con.commit()
        else:
            raise errors.StoreError
