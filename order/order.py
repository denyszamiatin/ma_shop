"""Order CRUD realisation"""

import psycopg2
import datetime
from config import DATABASE
from products import products


def add_order(conn, id_product, id_user, price, date):
    """
    Add order
    :param conn:
    :param id_product:
    :param id_user:
    :param price:
    :param date:
    :return: None
    """
    with conn.cursor() as cursor:
        price = products.get_product_price(conn, id_product)
        current_date = datetime.date.today()
        cursor.execute(f"""insert into Order_ 
            (id_user, id_product, price, date) values ('{id_user}', '{id_product}','{price}','{current_date}')""")
        conn.commit()


def get_order(conn, id_order):
    """
    get order
    :param conn:
    :param id_order:
    :return:
    """
    with conn.cursor() as cursor:
        cursor.execute(f"select * from Order_ where id_order='{id_order}'")
        try:
            return cursor.fecthone()
        except TypeError:
            raise KeyError

def delete_order(conn, id_order):
    """
    :param conn:
    :param id_order:
    :return:
    """
    with conn.cursor() as cursor:
        cursor.execute(f"select * from Order_ where id_order='{id_order}'")
        try:
            cursor.fecthone()
            cursor.execute(f"delete from Order_ where id_order='{id_order}'")
        except TypeError:
            raise ValueError
