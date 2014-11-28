# -*- coding: utf-8 -*-
"""
    crm.admin.views.auth
    ----------------

    crm panel admin auth views
"""

from flask import render_template, request, g, redirect, Blueprint
from flask_security.utils import login_user, logout_user

from crm.models_admin.user import User
from ..helpers import login_required, save_activity


bp = Blueprint('auth', __name__, template_folder='templates')


@bp.after_request
def check_response(response):
    """Save in the activity log the request result
    """
    return save_activity(response)


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