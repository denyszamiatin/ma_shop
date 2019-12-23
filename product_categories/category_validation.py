"""data validation module"""
from string import punctuation
import re

from app_config import CATEGORY_MAX_LENGTH


def validator(category):
    if not category.isalpha() or len(category) > CATEGORY_MAX_LENGTH:
        return False
    return True
