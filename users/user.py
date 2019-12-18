"""User crud"""


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
        try:
            cursor.execute(f'INSERT INTO users (first_name, second_name, email, password) '
                           f'VALUES ({first_name}, {second_name}, {email},crypt({password},gen_salt("md5"))')
            con.commit()
        except TypeError:
            raise ValueError


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
            raise ValueError


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
            raise ValueError
        if not cursor.rowcount:
            raise TypeError
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
            cursor.execute(f'update users set first_name = {first_name},'
                           f' second_nam = {second_name} where id = {user_id}')
        except TypeError:
            raise ValueError
        if not cursor.rowcount:
            raise TypeError
        con.commit()
