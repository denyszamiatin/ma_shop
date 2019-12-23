"""data validation module"""
from string import punctuation
import re

from app_config import NAME_MAX_LENGTH, PASSWORD_MAX_LENGTH


def email_validator(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    return False


def name_validator(name):
    if not name.isalpha() or len(name) > NAME_MAX_LENGTH:
        return False
    return True


def password_validator(password):
    if len(password) > PASSWORD_MAX_LENGTH:
        return False
    characters_allowed = [".", "_", "-"]
    for letter in password:
        if letter in punctuation and letter not in characters_allowed:
            return False
    return True


def register_form_validation(first_name, second_name, email, password):
    if (name_validator(first_name) and
            name_validator(second_name) and
            email_validator(email) and
            password_validator(password)):
        return True
    return False


def login_form_validation(email, password):
    if email_validator(email) and password_validator(password):
        return True
    return False
