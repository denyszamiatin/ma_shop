import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = 'static/img'
    THUMBNAIL_SIZE = (120, 70)
    PRODUCT_NAME_MAX_LENGTH = 1000
    PRODUCT_IMAGE_MAX_LENGTH = 1000
    PRODUCT_THUMBNAIL_MAX_LENGTH = 1000



DATABASE = {
    "database": "ma_shop",
    "user": "ma_admin",
    "password": "test_password",
    "host": "localhost",
    "port": 5432
}
