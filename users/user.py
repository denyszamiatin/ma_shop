"""User crud"""
import hashlib
from errors import errors

def add(con, first_name: str, second_name: str, email: str, password: str) -> None:
    """
    Add user to users table
    :param con: connection
    :param first_name: first user name
    :param second_name: second user name
    :param email: user email
    :param password: user password
    :return: None
    """
    with con.cursor() as cursor:
        hash_pass = hashlib.md5(password.encode('utf-8'))
        try:
            cursor.execute(f"insert into users (first_name, second_name, email, password) "
                           f"VALUES ('{first_name}', '{second_name}', '{email}', '{hash_pass.hexdigest()}')")
            con.commit()
        except TypeError:
            raise errors.StoreError


def read(con, user_id: int) -> str:
    """
    Get user by id
    :param con: connection
    :param user_id: id of user
    :return: str
    """
    with con.cursor() as cursor:
        cursor.execute(f'select first_name, second_name from users where id={user_id}')
        try:
            return cursor.fetchone()[0]
        except TypeError:
            raise errors.StoreError

def login(con, email, password) -> int:
    """
    Get user by email and check password
    :param con: connection
    :param email: user email
    :param password: user password
    :return: user id or raise error
    """
    with con.cursor() as cursor:
        cursor.execute(f"select id, password from users where email='{email}'")
        data = cursor.fetchone()
        try:
            hash_password = hashlib.md5(password.encode('utf-8'))
            if data[1] == hash_password.hexdigest():
                return data[0]
            raise errors.StoreError
        except TypeError:
            raise errors.StoreError


def delete(con, user_id: int) -> None:
    """
    Delete user by id
    :param con: connection
    :param user_id: id of user
    :return: None
    """
    with con.cursor() as cursor:
        try:
            cursor.execute(f'delete from users where id = {user_id}')
        except TypeError:
            raise errors.StoreError
        if not cursor.rowcount:
            raise errors.StoreError
        con.commit()


def update_name(con, first_name: str, second_name: str, user_id: int) -> None:
    """
    Update user name by id
    :param con: connection
    :param first_name: first user name
    :param second_name: second user name
    :param user_id: id user
    :return: None
    """
    with con.cursor() as cursor:
        try:
            cursor.execute(f"update users set first_name = '{first_name}',"
                           f" second_nam = '{second_name}' where id = {user_id}")
        except TypeError:
            raise errors.StoreError
        if not cursor.rowcount:
            raise errors.StoreError
        con.commit()
