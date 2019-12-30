import psycopg2

from app.config import DATABASE
from app.db_utils.db_utils_func import init_tables

if __name__ == "__main__":
    con = psycopg2.connect(**DATABASE)
    with con.cursor() as cursor:
        try:
            init_tables(cursor)
            con.commit()
        finally:
            if con:
                con.close()
