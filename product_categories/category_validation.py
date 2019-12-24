"""data validation module"""
from app_config import CATEGORY_MAX_LENGTH


def validator(category_name):
    return category_name.isalpha() and len(category_name) <= CATEGORY_MAX_LENGTH
