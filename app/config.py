import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "3123123123"


"""App config variables"""
NAME_MAX_LENGTH = 50
PASSWORD_MAX_LENGTH = 50
CATEGORY_MAX_LENGTH = 50
PRODUCT_MAX_LENGTH = 50
