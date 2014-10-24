# -*- coding: utf-8 -*-
"""
    crm.admin.views
    ----------------

    Admin controllers
"""

from flask import Blueprint, request, render_template, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user

from crm.models.permission import Permission
from crm.models.role import Role
from crm.models.company import Company
from crm.models.admin import Admin
from crm.models.user import User
from crm.core import login_manager

import json

bp = Blueprint('admin', __name__, template_folder='templates')


@bp.route('/permissions', methods=['GET'])
@login_required
def permissions():
    """
    Return a list with all the system permissions
    """

    result = Permission.get_all()

    return render_template('permissions.html', permissions=result)


@bp.route('/permissions', methods=['POST'])
@login_required
def create_permissions():
    """
    Create a new permission
    """

    data = request.get_json()
    p = Permission()
    p.set_name(data['name'])
    p.set_description(data['description'])
    result = Permission.save_object(p)

    return result


@bp.route('/permissions/<p_id>', methods=['GET'])
@login_required
def read_permission(p_id):
    """
    Return specified permission
    """

    result = Permission.get_object(p_id)

    return result


@bp.route('/permissions/<p_id>', methods=['POST'])
@login_required
def update_permission(p_id):
    """
    Update specified permission
    """

    data = request.get_json()
    p = Permission.objects.get(id=p_id)
    p.set_name(data['name'])
    p.set_description(data['description'])
    result = Permission.save_object(p)

    return result


@bp.route('/permissions/<p_id>', methods=['DELETE'])
@login_required
def delete_permission(p_id):
    """
    Delete specified permission
    """

    result = Permission.delete_object(p_id)

    return result


@bp.route('/roles', methods=['GET'])
@login_required
def roles():
    """
    Return a list with all the system roles
    """

    r = Role.get_all()
    p = Permission.get_all()

    return render_template('roles.html', roles=r, permissions=p)


@bp.route('/roles', methods=['POST'])
@login_required
def create_role():
    """
    Create a new role

    """

    data = request.get_json()
    r = Role()
    r.set_name(data['name'])
    r.set_description(data['description'])
    perms = json.loads(data['permissions'])
    result = Role.save_object(r, perms)

    return result


@bp.route('/roles/<r_id>', methods=['GET'])
@login_required
def read_role(r_id):
    """
    Return specified role
    """

    result = Role.get_object(id=r_id)

    return result


@bp.route('/roles/<r_id>', methods=['POST'])
@login_required
def update_role(r_id):
    """
    Update specified role
    """

    data = request.get_json()
    r = Role.objects.get(id=r_id)
    r.set_name(data['name'])
    r.set_description(data['description'])
    perms = json.loads(data['permissions'])
    result = Role.save_object(r, perms)

    return result


@bp.route('/roles/<r_id>', methods=['DELETE'])
@login_required
def delete_role(r_id):
    """
    Delete specified permission
    """

    result = Role.delete_object(r_id)

    return result


@bp.route('/companies', methods=['GET'])
@login_required
def companies():
    """
    Return a list with all the system companies
    """

    c = Company.get_all()

    return render_template('companies.html', companies=c)


@bp.route('/companies', methods=['POST'])
@login_required
def create_company():
    """
    Create a new company
    """

    data = request.get_json()
    compa = Company()
    admin = Admin()

    compa.set_name(data['name'])
    compa.set_direction(data['direction'])

    admin.set_name(data['admin_name'])
    admin.set_email(data['admin_email'])
    admin.set_role(Role.objects.get(name='Company administrator'))
    admin.set_password('12345678')  # TODO: autogenerate password, send mail

    result = Company.save_object(compa, admin)

    return json.dumps(result)

@bp.route('/companies/<c_id>', methods=['GET'])
@login_required
def read_company(c_id):
    """
    Return specified company
    """

    result = Company.get_object(id=c_id)

    return result


@bp.route('/companies/<c_id>', methods=['POST'])
@login_required
def update_company(c_id):
    """
    Update specified company and their administrator
    """

    data = request.get_json()
    compa = Company.objects.get(id=c_id)
    admin = compa.get_admin()

    compa.set_name(data['name'])
    compa.set_direction(data['direction'])

    admin.set_name(data['admin_name'])
    admin.set_email(data['admin_email'])

    result = Company.save_object(compa, admin, edit=True)

    return json.dumps(result)


@bp.route('/companies/<c_id>', methods=['DELETE'])
@login_required
def delete_company(c_id):
    """
    Delete specified company and their admin
    """

    result = Company.delete_object(c_id)

    return result

@bp.route('/users', methods=['GET'])
@login_required
def users():
    """
    Get all API Admin users
    """

    u = User.get_all('Administrator API panel')

    return render_template('users.html', users=u)


@bp.route('/users', methods=['POST'])
@login_required
def create_user():
    """
    Create a new API admin user

    """
    data = request.get_json()
    user = User()

    user.set_name(data['name'])
    user.set_email(data['email'])
    user.set_password(data['password'])
    user.set_role(Role.objects.get(name='Administrator API panel'))

    result = User.save_object(user)

    return result


@bp.route('/users/<u_id>', methods=['GET'])
@login_required
def read_user(u_id):
    """
    Return specified user
    """

    result = User.get_object(id=u_id)

    return result


@bp.route('/users/<u_id>', methods=['POST'])
@login_required
def update_user(u_id):
    """
    Update an API admin user

    """
    data = request.get_json()
    u = User.objects.get(id=u_id)

    u.set_name(data['name'])
    u.set_email(data['email'])
    u.set_password(data['password'])

    result = User.save_object(u)

    return result


@bp.route('/users/<u_id>', methods=['DELETE'])
@login_required
def delete_user(u_id):
    """
    Delete specified user
    """

    result = User.delete_object(u_id)

    return result


@bp.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.objects.get(
        email=email,  # TODO: hacer email unico
        role=Role.objects.get(name='Administrator API panel'))
    print 'passwords', password, user.get_password()
    if user.get_password() == password:
        login_user(user)
        return render_template('companies.html')
    else:
        errors = {'errors':'datos incorrectos'}
        return render_template('login.html', errors=errors)


@bp.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return render_template('login.html')


@login_manager.user_loader
def load_user(userid):
    print 'load_user'
    user = User.objects.get(id=userid)

    if user:
        return user
    else:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    errors = "The server could not verify that you are authorized to access the URL requested." \
          " You either supplied the wrong credentials (e.g. a bad password), " \
          "or your browser doesn't understand how to supply the credentials required."
    return render_template('login.html', errors=errors)
