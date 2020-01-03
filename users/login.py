from flask import session, redirect, flash, url_for
from functools import wraps


def login_required(function):
    """Wrap route and check check is user logined"""
    @wraps(function)
    def wrap(*args, **kwargs):
        if 'user_id' in session:
            return function(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap
