import os

DATABASE = {
    "database": "ma_shop",
    "host": "localhost",
    "user": "ma_admin",
    "password": "1",
    "port": 5432
}

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

FIXTURES_PATH = os.path.join(PROJECT_PATH, "fixtures")
