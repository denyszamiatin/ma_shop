import psycopg2
import pytest

import products.products as products
from app.config import DATABASE
from errors.errors import StoreError


def test_create_product():
    con = psycopg2.connect(**DATABASE)
    products.add_product(con, 'Bed', 3000,
                              'https://www.westelm.com/weimgs/ab/images/wcm/products/201940/0467/wright-bed-c.jpg')
    assert products.get_product(con, 1) == "Bed"


def test_update_product():
    con = psycopg2.connect(**DATABASE)
    products.add_product(con, 'Bed', 3000,
                              'https://www.westelm.com/weimgs/ab/images/wcm/products/201940/0467/wright-bed-c.jpg')
    products.edit_product(con, 2, 5100)
    assert products.get_product_price(con, 2) == 5100


def test_delete_product():
    con = psycopg2.connect(**DATABASE)
    products.add_product(con, 'Bed', 3000,
                              'https://www.westelm.com/weimgs/ab/images/wcm/products/201940/0467/wright-bed-c.jpg')
    products.delete_product(con, 4)
    with pytest.raises(StoreError):
        products.get_product(con, 4)
