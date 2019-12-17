"""
CRUD
"""


def add(conn, user_id: int, product_id: int) -> None:
    """
    Add new prodact and
    user id to cart.
    :param conn: str
    :param user_id: int
    :param product_id: int
    :return: None
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""INSERT INTO cart(user_id, product_id)
                            VALUES ({user_id}, {product_id})""")
    conn.commit()


def get_all(conn, user_id: int) -> list:
    """
    Get all products_id from db using index user_id.
    :param conn: str
    :param user_id: int
    :return: list
    """
    cursor = conn.cursor()
    cursor.execute(f"""SELECT product_id FROM cart
                    WHERE user_id = {user_id}""")
    result = cursor.fetchall()
    cursor.close()
    return [''.join(i) for i in result]


def delete(conn, user_id, product_id) -> None:
    """
    Delete task in db.
    :param conn: str
    :param user_id: int
    :param product_id: int
    :return: None
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""DELETE FROM cart 
                        WHERE (user_id, product_id) VALUES ({user_id}, {product_id})""")
    conn.commit()


def delete_all(conn, user_id) -> None:
    """
    Delete task in db.
    :param conn: str
    :param user_id: int
    :return: None
    """
    with conn.cursor() as cursor:
        cursor.execute(f"""DELETE FROM cart 
                        WHERE user_id = {user_id}""")
    conn.commit()
