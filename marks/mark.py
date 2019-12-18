"""Module to precess rating of the products"""


def add(conn, id_user: int, id_product: int, mark: int) -> :
    """Add mark to the database. Used by User"""
    with conn.cursor() as cursor:
        try:
            cursor.execute(f"""
                INSERT INTO mark (id_user, id_product, rating)
                VALUES ('{id_user}', '{id_product}', '{mark}')
                """)
        except TypeError:
            raise ValueError


def average_rating(conn, id_product: int):
    """Return average rating of the product with id = product_id"""
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""select avg(rating) FROM mark WHERE id_product = '{id_product}'""")
            avg = cursor.fetchone()[0]
        return avg
    except ValueError:
        raise ValueError
