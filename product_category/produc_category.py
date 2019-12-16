import psycopg2
from config import DATABASE

with psycopg2.connect(dbname=DATABASE["database"], user=DATABASE["user"],
                      password=DATABASE["password"]) as conn:
    def create_category(name: str) -> None:
        """
        Create new category
        name: new category name
        """
        with conn.cursor() as cursor:
            try:
                cursor.execute("insert into product_category (name) values('{0}')".format(name))
                conn.commit()
            except psycopg2.errors.UniqueViolation:
                raise KeyError

    def read_category(id: int) -> str:
        """
        Read category from DB
        id: category id in DB
        """
        with conn.cursor() as cursor:
            cursor.execute("select name from product_category where id = {0}".format(id))
            try:
                return cursor.fetchone()[0]
            except TypeError:
                raise KeyError

    def update_category(id: int, new_name: str) -> None:
        """
        Update category in DB
        id: category id in DB
        new_name: category new name
        """
        with conn.cursor() as cursor:
            cursor.execute("select name from product_category where id = {0}".format(id))
            if cursor.fetchone():
                cursor.execute("update product_category set name = '{0}' where id = {1}".format(new_name, id))
                conn.commit()
            else:
                raise KeyError

    def delete_category(id: int) -> None:
        """
        Delete category from DB
        id: category id in DB
        """
        with conn.cursor() as cursor:
            cursor.execute("select name from product_category where id = {0}".format(id))
            if cursor.fetchone():
                cursor.execute("delete from product_category where id = {0}".format(id))
                conn.commit()
            else:
                raise KeyError
