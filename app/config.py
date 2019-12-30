import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = 'static/img'
    THUMBNAIL_SIZE = (120, 70)
    PRODUCT_NAME_MAX_LENGTH = 1000


DATABASE = {
    "database": "ma_shop",
    "user": "ma_admin",
    "password": os.environ.get('OLD_DATABASE_PASS'),
    "host": "localhost",
    "port": 5432
}

"""App config variables"""
NAME_MAX_LENGTH = 50
PASSWORD_MAX_LENGTH = 50
CATEGORY_MAX_LENGTH = 50

PRODUCT_MAX_LENGTH = 50