"""data validation module"""


def validator(category_name):
    return category_name.isalpha() and len(category_name) <= 3000
