"""Order CRUD realisation"""

import datetime
from products import products
import errors.errors as errors


def add(conn, id_product, id_user, id_order, price, date):
    '''
    Add order to archive
    '''
    with conn.cursor() as cursor:
        price = products.get_product_price(conn, id_product)
        current_date = datetime.date.today()
        cursor.execute(f"""insert into order_archive (id_user, id_order, id_product,  price, date_archive)
                           values ('{id_user}','{id_order}' '{id_product}','{price}','{current_date}')""")
        conn.commit()


def get(conn, archive_id):
    '''
    Read archive from DB
    '''
    with conn.cursor() as cursor:
        cursor.execute(f"select price, date_archive from order_archive where archive_id='{archive_id}'")
        try:
            return cursor.fetchone()[0]
        except TypeError:
            raise errors.StoreError

