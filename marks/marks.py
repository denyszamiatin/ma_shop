"""Module to precess rating of the products"""
from datetime import datetime


def add_mark(cursor, id_user, id_product, mark):
    """Add mark to the database. Used by User"""
    TIME = datetime.now()
    cursor.execute("""
        insert into mark (id_user, id_product, mark_date, rating)
        values ('{}', '{}', '{}', '{}')
        """.format(id_user, id_product, TIME, mark))


def average_rating(cursor, id_product: int):
    """Return average rating of the product with id = product_id"""
    cursor.execute(f"""select rating from mark where id_product = '{id_product}'""")
    marks = cursor.fetchall()
    avg = round(sum(m[0] for m in marks)/len(marks), 1)
    return avg
