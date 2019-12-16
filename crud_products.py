"""
CRUD properties implementation
"""
from datetime import date
from typing import List


def add_product(con, product_name: str, price: int, img: str) -> None:
    """
    Add new task to db.
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


def get_product(con, id: int) -> str:
    """
    Get product from db using index parameter.
    :param con: str
    :param id: int
    :return: str
    """
    cursor = con.cursor()
    cursor.execute("""SELECT productname FROM postgres.public.products
                    WHERE productid = {0}""".format(id))
    result = cursor.fetchone()
    cursor.close()
    return result[0]


