# -*- coding: utf-8 -*-
"""
    crm.admin.views.user
    ----------------

    crm panel admin user views
"""

import json

from flask import request, render_template, g, redirect, Blueprint
from flask_security.core import current_user

from crm.models2.permission import Permission
from crm.models2.role import Role
from crm.models2.company import Company
from crm.models2.admin import Admin
from crm.models2.user import User
from crm.models2.log import Log
from ..helpers import login_required


bp = Blueprint('user', __name__, template_folder='templates')


@bp.route('/users', methods=['GET'])
@login_required
def users():
    """Get all API Admin users
    """
    result = User.get_all('Administrator API panel')
    setattr(g, 'result', result)
    return render_template('users.html', users=result)


@bp.route('/users', methods=['POST'])
@login_required
def create_user():
    """Create a new API admin user
    """
    data = request.get_json()
    user = User()
    password = data['password']
    user.set_name(data['name'])
    user.set_email(data['email'])
    user.set_password(User.encrypt(data['password']))
    user.generate_auth_token()
    user.add_role(Role.objects.get(name='Administrator API panel'))
    # user.admin = Admin() # TODO: agregar una companía al superusuario
    result = User.save_object(user, password, mail=True)
    setattr(g, 'result', result)
    return result


@bp.route('/users/<user_id>', methods=['GET'])
@login_required
def read_user(user_id):
    """Return specified user
    """
    result = User.get_object(id=user_id)
    setattr(g, 'result', result)
    return result


@bp.route('/users/<user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    """Update an API admin user
    """
    data = request.get_json()
    u = User.objects.get(id=user_id)
    password = data['password']
    u.set_name(data['name'])
    u.set_email(data['email'])
    u.set_password(User.encrypt(data['password']))
    result = User.save_object(u, password, mail=False)
    setattr(g, 'result', result)
    return result


@bp.route('/users/<user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Delete specified user
    """
    result = User.delete_object(user_id)
    setattr(g, 'result', result)
    return result
