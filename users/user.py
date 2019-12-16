

def add(con, first_name: str, second_name: str, email: str, password: str) -> None:
    with con.cursor() as cursor:
        try:
            cursor.execute(f'INSERT INTO user (first_name, last_name, email, password) '
                           f'VALUES ({first_name}, {second_name}, {email}, {password})')
            con.commit()
        except TypeError: #C   HANGE!
            raise ValueError #CHANGE!


def read(con, user_id: int) -> str:
    with con.cursor() as cursor:
        cursor.execute(f'SELECT first_name, second_name FROM user WHERE id={user_id}')
        try:
            return cursor.fetchone()[0]
        except TypeError:
            raise ValueError #CHANGE!


def delete(con, user_id: int) ->str:
    with con.cursor() as cursor:
        cursor.execute(f'SELECT first_name, second_name FROM user WHERE id={user_id}')
        if cursor.rowcount:
            try:
                cursor.execute(f'DELETE FROM user WHERE id = {user_id}')
            except TypeError:
                raise ValueError #CHANGE!
        else:#CHANGE!
            raise ValueError #CHANGE!

def update_name(con, first_name:str , second_name: str, user_id: int) ->:
    with con.cursor() as cursor:
        cursor.execute(f'SELECT first_name, second_name FROM user WHERE id={user_id}')
        if cursor.rowcount:
            try:
                cursor.execute(f'UPDATE user SET first_name = {first_name},'
                               f' second_nam = {second_name} WHERE id = {user_id}')
            except TypeError:
                raise ValueError #CHANGE!
            else:
                raise ValueError  #CHANGE!