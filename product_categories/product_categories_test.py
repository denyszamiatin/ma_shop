import pytest
import psycopg2

import product_categories
from config import DATABASE


def create_category():
    conn = psycopg2.connect(**DATABASE)
    product_categories.create_category(conn, "Soldering irons")
    assert product_categories.read_category(conn, 1) == "Soldering irons"


