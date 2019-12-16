import datetime

import psycopg2
import pytest

import crud_products
from config import DATABASE


def test_create_product():
    con = psycopg2.connect(**DATABASE)
    crud_products.add_product(con, 'Bed', 3000,
                              'https://www.westelm.com/weimgs/ab/images/wcm/products/201940/0467/wright-bed-c.jpg')
    assert crud_products.get_product(con, 13) == "Bed"

