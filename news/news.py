"""This module provides model of news creation, reading and update"""
import datetime
import psycopg2
from errors import errors


def add(connection, title: str, post: str, id_user: int, author: str) -> None:
    """Add new post to news table"""
    with connection.cursor() as cursor:
        try:
            cursor.execute(f'insert into news (title, post, id_user, news_date, author) '
                           f'values ({title}, {post}, {id_user}, {datetime.date.today()}, {author})')
            connection.commit()
        except psycopg2.DatabaseError:
            raise errors.StoreError


def read(connection, news_id: int) -> str:
    """Read the post from news table by news_id"""
    with connection.cursor() as cursor:
        cursor.execute(f'select title, post, news_date, author from news where id={news_id}')
        try:
            return cursor.fetchone()
        except TypeError:
            raise errors.StoreError


def get_all_news(connection) -> str:
    """Read the post from news table by news_id"""
    with connection.cursor() as cursor:
        cursor.execute(f'select title, post, news_date, author from news')
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
