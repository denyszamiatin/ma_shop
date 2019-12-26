"""
CRUD
"""


def add(conn, user_id: int, product_id: int) -> None:
    """
    Add new product and
    user id to cart.
    :param conn: str
    :param user_id: int
    :param product_id: int
    :return: None
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""insert into cart(id_user, id_product)
                            values ({user_id}, {product_id})""")
    conn.commit()


def get_all(conn, user_id: int) -> list:
    """
    Get all products_id from db using index user_id.
    :param conn: str
    :param user_id: int
    :return: list
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""select id_product from cart
                        where id_user = {user_id}""")
        result = cursor.fetchall()
    return [i[0] for i in result]


def delete(conn, user_id, product_id) -> None:
    """
    Delete task in db.
    :param conn: str
    :param user_id: int
    :param product_id: int
    :return: None
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""delete from cart 
                        where id_user = {user_id} and id_product = {product_id}""")
    conn.commit()


def delete_all(conn, user_id) -> None:
    """
    Delete task in db.
    :param conn: str
    :param user_id: int
    :return: None
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""delete from cart 
                        where id_user = {user_id}""")
    conn.commit()
