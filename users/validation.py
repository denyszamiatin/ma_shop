"""data validation module"""
import string

def register_form_validation(first_name, second_name, email, password):
    if not first_name.isalpha() or len(first_name) > 35:
        return False
    if not second_name.isalpha() or len(second_name) > 50:
        return False

    if list(email).count("@") != 1 or len(email) > 50:
        return False
    characters_allowed = [".", "_", "@", "-"]
    for letter in email:
        if letter in string.punctuation and letter not in characters_allowed:
            return False

    if len(password) > 100:
        return False
    for letter in password:
        if letter in string.punctuation and letter not in characters_allowed:
            return False

    return True
