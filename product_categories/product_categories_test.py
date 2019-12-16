import pytest
import psycopg2

import product_categories
from config import DATABASE

with psycopg2.connect(**DATABASE) as conn:

    def create_category():
        product_categories.create_category(conn, "Soldering irons")
        assert product_categories.read_category(conn, 1) == "Soldering irons"

    def update_category():
        product_categories.create_category(conn, "furniturka")
        product_categories.update_category(conn, 2, "Furniture")
        assert product_categories.read_category(conn, 2) == "Furniture"

    def delete_category():
        product_categories.create_category(conn, "Wears")
        product_categories.delete_category(conn, 3)
        with pytest.raises(KeyError):
            product_categories.read_category(conn, 3)

