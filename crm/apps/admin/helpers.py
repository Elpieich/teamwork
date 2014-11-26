# -*- coding: utf-8 -*-

from functools import wraps

from flask import render_template
from flask_security.core import current_user


def login_required(func):
    """Login decorator that verifies the user
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated():
            return unauthorized()
        return func(*args, **kwargs)
    return decorated_view


def unauthorized():
    """Return a message to the unauthorized user
    """
    errors = "The server could not verify that you are authorized to access the URL requested." \
             " You either supplied the wrong credentials (e.g. a bad password), " \
             "or your browser doesn't understand how to supply the credentials required."

    return render_template('login.html', errors=errors)
