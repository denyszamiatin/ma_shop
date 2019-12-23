import psycopg2

from config_.config_ import DATABASE
from db_utils.db_utils_func import clear_tables, drop_tables

if __name__ == "__main__":
    con = psycopg2.connect(**DATABASE)
    with con.cursor() as cursor:
        try:
            clear_tables(cursor)
            drop_tables(cursor)
            con.commit()
        finally:
            if con:
                con.close()
