from pathlib import Path
from environs import Env

basedir = Path(Path(__file__).parent).resolve()
env = Env()
env.read_env()


class Config(object):

    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = env.str("SECRET_KEY")
    UPLOAD_FOLDER = 'static/img'
    THUMBNAIL_SIZE = (120, 70)
    PRODUCT_NAME_MAX_LENGTH = 1000
    SMTP_SERVER = "localhost"
    ADMIN_EMAIL = "admin@ma_shop.org"


DATABASE = {
    "database": "ma_shop",
    "user": "ma_admin",
    "password": env.str('OLD_DATABASE_PASS'),
    "host": "localhost",
    "port": 5432
}

"""App config variables"""
NAME_MAX_LENGTH = 50
PASSWORD_MAX_LENGTH = 50
CATEGORY_MAX_LENGTH = 50

PRODUCT_MAX_LENGTH = 50

ITEMS_PER_PAGE = 10
