# -*- coding: utf-8 -*-
"""
    crm.admin.login
    ----------------

    login controller
"""

from functools import wraps

from flask import render_template, request, g, redirect
from flask_security.utils import login_user, logout_user
from flask_security.core import current_user

from crm.models2.user import User
from crm.models2.log import Log

from . import bp


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


@bp.after_request
def check_response(response):
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


@bp.route('/login', methods=['POST'])
def login():
    """Verify the information to log in an user
    """

    setattr(g, 'result', 'login')
    email = request.form['email']
    password = request.form['password']

    user = User.get_admin(email)

    if 'errors' in user:
        errors = 'Please verify your email and password'
        return render_template('login.html', errors=errors)

    if user.is_correct_password(password):
        login_user(user, remember=False)
        # return companies()
        return redirect('/admin/companies')
    else:
        errors = 'Please verify your email and password'
        return render_template('login.html', errors=errors)


@bp.route('/login', methods=['GET'])
@login_required
def re_login():
    """Return to the index
    """

    setattr(g, 'result', 're-login')
    return redirect('/admin')


@bp.route("/logout", methods=['GET'])
@login_required
def logout():
    """Log out the current_user
    """

    setattr(g, 'result', 'logout')
    logout_user()
    return render_template('login.html')