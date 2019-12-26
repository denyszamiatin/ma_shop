"""This module provides model of news creation, reading and update"""
import psycopg2

from errors import errors


def add(connection, title: str, post: str, id_user: int) -> None:
    """Add new post to news table"""
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"""insert into news(title, post, id_user) 
                                values ({title}, {post}, {id_user})""")
            connection.commit()
        except psycopg2.DatabaseError:
            raise errors.StoreError


def read(connection, news_id: int) -> str:
    """Read the post from news table by news_id"""
    with connection.cursor() as cursor:
        cursor.execute(f'select title, post, news_date, first_name, second_name '
                       f'from news n inner join users u on n.id_user = u.id '
                       f'where n.id = {news_id}')
        try:
            return cursor.fetchone()
        except TypeError:
            raise errors.StoreError


def get_all(connection) -> str:
    """Read all posts"""
    with connection.cursor() as cursor:
        cursor.execute(f'select n.id, title, post, news_date, first_name, second_name '
                       f'from news n inner join users u on n.id_user = u.id;')
        try:
            return cursor.fetchall()
        except TypeError:
            raise errors.StoreError


def update_title(connection, title: str, news_id: int) -> None:
    """Update the title of news input in the news table by news_id"""
    with connection.cursor() as cursor:
        cursor.execute(f'update news set post = {title} where id = {news_id}')
        if cursor.rowcount:
            connection.commit()
        else:
            raise errors.StoreError


def update_post(connection, post: str, news_id: int) -> None:
    """Update the news input in the news table by news_id"""
    with connection.cursor() as cursor:
        cursor.execute(f'update news set post = {post} where id = {news_id}')
        if cursor.rowcount:
            connection.commit()
        else:
            raise errors.StoreError


def delete(conn, news_id: int) -> None:
    """
    Delete news from DB
    """
    with conn.cursor() as cursor:
        cursor.execute(f"delete from news where id = {news_id}")
        if cursor.rowcount:
            conn.commit()
        else:
            raise errors.StoreError


def edit_news(conn, news_id: int, title: str, post: str) -> None:
    """Update the news input in the news table by news_id"""
    with conn.cursor() as cursor:
        cursor.execute("""update news
                           set title = '{0}', post = '{1}'
                           where id = '{2}'""".format(title, post, news_id))
        if cursor.rowcount:
            conn.commit()
        else:
            raise errors.StoreError
