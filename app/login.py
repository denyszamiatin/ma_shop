from flask import session, redirect, flash, url_for, request
from functools import wraps
from .models import Users


def login_required(function):
    """Wrap route and check check is user logined"""
    @wraps(function)
    def wrap(*args, **kwargs):
        if 'user_id' in session:
            return function(*args, **kwargs)
        else:
            session["next_page"] = request.path
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


def admin_role_required(function):
    """Wrap route and check is logined user admin"""
    @wraps(function)
    def wrap(*args, **kwargs):
        user = Users.query.filter_by(id=session["user_id"]).first()
        if user.admin_role:
            return function(*args, **kwargs)
        flash("You don't have admin privileges")
        return redirect(url_for("index"))
    return wrap
