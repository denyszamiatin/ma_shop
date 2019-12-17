import psycopg2
import pytest

from products import products
from db_utils.config import DATABASE


def test_create_product():
    con = psycopg2.connect(**DATABASE)
    products.add_product(con, 'Bed', 3000,
                              'https://www.westelm.com/weimgs/ab/images/wcm/products/201940/0467/wright-bed-c.jpg')
    assert products.get_product(con, 14) == "Bed"


def test_update_product():
    con = psycopg2.connect(**DATABASE)
    products.add_product(con, 'Bed', 3000,
                              'https://www.westelm.com/weimgs/ab/images/wcm/products/201940/0467/wright-bed-c.jpg')
    products.edit_product(con, 16, 5100)
    assert products.get_product_price(con, 16) == 5100


def test_delete_product():
    con = psycopg2.connect(**DATABASE)
    products.add_product(con, 'Bed', 3000,
                              'https://www.westelm.com/weimgs/ab/images/wcm/products/201940/0467/wright-bed-c.jpg')
    products.delete_product(con, 17)
    with pytest.raises(TypeError):
        products.get_product(con, 17)
