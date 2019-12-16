"""
CRUD properties implementation
"""


def add_product(con, product_name: str, price: int, img: str) -> None:
    """
    Add new product to db.
    :param con: str
    :param product_name: str
    :param price: int
    :param img: str
    :return: None
    """
    with con.cursor() as cursor:
        cursor.execute("""INSERT INTO postgres.public.products(productname, price, image)
                            VALUES ('{0}', '{1}', '{2}')""".format(product_name, price, img))
    con.commit()


def get_product(con, product_id: int) -> str:
    """
    Get product from db using index parameter.
    :param con: str
    :param product_id: int
    :return: str
    """
    cursor = con.cursor()
    cursor.execute("""SELECT productname FROM postgres.public.products
                    WHERE productid = {0}""".format(product_id))
    result = cursor.fetchone()
    cursor.close()
    return result[0]


def get_product_price(con, product_id: int) -> str:
    """
    Get product from db using index parameter.
    :param con: str
    :param product_id: int
    :return: str
    """
    cursor = con.cursor()
    cursor.execute("""SELECT price FROM postgres.public.products
                    WHERE productid = {0}""".format(product_id))
    result = cursor.fetchone()
    cursor.close()
    return result[0]


def edit_product(con, product_id: int, new_price: int) -> None:
    """
    Update task in db.
    :param con: str
    :param new_price: int
    :param product_id: int
    :return: None
    """
    with con.cursor() as cursor:
        cursor.execute("""UPDATE postgres.public.products
                        SET price = '{0}'
                        WHERE productid = '{1}'""".format(new_price, product_id))
    con.commit()


def delete_product(con, product_id: int) -> None:
    """
    Delete task in db.
    :param con: str
    :param product_id: int
    :return: None
    """
    with con.cursor() as cursor:
        cursor.execute("""DELETE FROM postgres.public.products 
                        WHERE productid = {0}""".format(product_id))
    con.commit()
