# -*- coding: utf-8 -*-

from functools import wraps

from flask import render_template, request, g
from flask_security.core import current_user

from crm.models_admin.log import Log
from crm.models_admin.user import User


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


def save_activity(response):
    """Save in the activity log the request result
    """
    if current_user.is_active():
        Log.save_object(
            request.remote_addr,
            request.url,
            request.method,
            User.objects.get(id=current_user.get_id()),
            getattr(g, 'result'))
    return response