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
            cursor.execute(f"""insert into Comments(id_product, id_user, body)
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
        cursor.execute(f"""select id_user, body, date from Comments where id_product={product_id}""")
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
        cursor.execute(f"""update Comments set body={body} where id={comment_id}""")
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
        cursor.execute(f"""delete from Comments where id={comment_id}""")
        if cursor.rowcount:
            con.commit()
        else:
            raise errors.StoreError
