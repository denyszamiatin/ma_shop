from app.config import PRODUCT_MAX_LENGTH


def valid(product_name, price):
    if not valid_alpha(product_name):
        return 'Product name incorrect'
    if not valid_max_length(product_name):
        return 'Product name too long'
    if not valid_digit(price):
        return 'Price incorrect'
    return 'Ok'


def valid_alpha(product_name):
    if product_name.isalpha():
        return True
    return False


def valid_max_length(product_name):
    if len(product_name) < PRODUCT_MAX_LENGTH:
        return True
    return False


def valid_digit(price):
    if price.isdigit():
        return True
    return False
