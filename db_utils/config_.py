import os

DATABASE = {
    "database": "ma_shop",
    "user": "pika",
    "host": "localhost",
    "password": "polohol",
    "port": 5432
}

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

FIXTURES_PATH = os.path.join(PROJECT_PATH, "fixtures")