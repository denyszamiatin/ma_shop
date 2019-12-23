"""data validation module"""
from app_config import CATEGORY_MAX_LENGTH


def validator(category_name):
    if not category_name.isalpha() or len(category_name) > CATEGORY_MAX_LENGTH:
        return False
    return True


def add_validation(category_name):
    if validator(category_name):
        return True
    return False
