# -*- coding: utf-8 -*-
"""
    crm.admin.views
    ----------------

    Admin controllers
"""

import json

from flask import request, render_template, g, redirect
from flask_security.core import current_user

from crm.models2.permission import Permission
from crm.models2.role import Role
from crm.models2.company import Company
from crm.models2.admin import Admin
from crm.models2.user import User
from crm.models2.log import Log
from login import login_required
from . import bp


@bp.route('/permissions', methods=['GET'])
@login_required
def permissions():
    """Return a list with all the system permissions
    """

    result = Permission.get_all()
    setattr(g, 'result', result)

    return render_template('permissions.html', permissions=result)


@bp.route('/permissions', methods=['POST'])
@login_required
def create_permissions():
    """Create a new permission
    """

    data = request.get_json()
    p = Permission()
    p.set_name(data['name'])
    p.set_description(data['description'])
    result = Permission.save_object(p)
    setattr(g, 'result', result)

    return result


@bp.route('/permissions/<p_id>', methods=['GET'])
@login_required
def read_permission(p_id):
    """Return specified permission
    """

    result = Permission.get_object(p_id)
    setattr(g, 'result', result)

    return result


@bp.route('/permissions/<p_id>', methods=['POST'])
@login_required
def update_permission(p_id):
    """Update specified permission
    """

    data = request.get_json()
    p = Permission.objects.get(id=p_id)
    p.set_name(data['name'])
    p.set_description(data['description'])
    result = Permission.save_object(p)
    setattr(g, 'result', result)

    return result


@bp.route('/permissions/<p_id>', methods=['DELETE'])
@login_required
def delete_permission(p_id):
    """Delete specified permission
    """

    result = Permission.delete_object(p_id)
    setattr(g, 'result', result)

    return result


@bp.route('/roles', methods=['GET'])
@login_required
def roles():
    """Return a list with all the system roles
    """

    r = Role.get_all()
    p = Permission.get_all()
    setattr(g, 'result', p)

    return render_template('roles.html', roles=r, permissions=p)


@bp.route('/roles', methods=['POST'])
@login_required
def create_role():
    """Create a new role
    """

    data = request.get_json()
    r = Role()
    r.set_name(data['name'])
    r.set_description(data['description'])
    perms = json.loads(data['permissions'])
    result = Role.save_object(r, perms)
    setattr(g, 'result', result)

    return result


@bp.route('/roles/<r_id>', methods=['GET'])
@login_required
def read_role(r_id):
    """Return specified role
    """

    result = Role.get_object(id=r_id)
    setattr(g, 'result', result)

    return result


@bp.route('/roles/<r_id>', methods=['POST'])
@login_required
def update_role(r_id):
    """Update specified role
    """

    data = request.get_json()
    r = Role.objects.get(id=r_id)
    r.set_name(data['name'])
    r.set_description(data['description'])
    perms = json.loads(data['permissions'])
    result = Role.save_object(r, perms)
    setattr(g, 'result', result)

    return result


@bp.route('/roles/<r_id>', methods=['DELETE'])
@login_required
def delete_role(r_id):
    """Delete specified permission
    """

    result = Role.delete_object(r_id)
    setattr(g, 'result', result)

    return result


@bp.route('/companies', methods=['GET'])
@login_required
def companies():
    """Return a list with all the system companies
    """

    result = Company.get_all()
    setattr(g, 'result', result)

    return render_template('companies.html', companies=result)


@bp.route('/companies', methods=['POST'])
@login_required
def create_company():
    """Create a new company
    """

    data = request.get_json()
    company = Company()
    admin = Admin()

    company.set_name(data['name'])
    company.set_direction(data['direction'])

    admin.set_name(data['admin_name'])
    admin.set_email(data['admin_email'])
    admin.add_role(Role.objects.get(name='Company administrator'))
    admin.generate_auth_token()
    password = User.generate_password()
    admin.set_password(User.encrypt(password))

    result = Company.save_object(company, admin, password, edit=False)
    setattr(g, 'result', json.dumps(result))

    return json.dumps(result)


@bp.route('/companies/<c_id>', methods=['GET'])
@login_required
def read_company(c_id):
    """Return specified company
    """

    result = Company.get_object(id=c_id)
    setattr(g, 'result', result)

    return result


@bp.route('/companies/<c_id>', methods=['POST'])
@login_required
def update_company(c_id):
    """Update specified company and their administrator
    """

    data = request.get_json()
    compa = Company.objects.get(id=c_id)
    admin = compa.get_admin()

    compa.set_name(data['name'])
    compa.set_direction(data['direction'])

    admin.set_name(data['admin_name'])
    admin.set_email(data['admin_email'])

    result = Company.save_object(compa, admin, None, edit=True)
    setattr(g, 'result', json.dumps(result))

    return json.dumps(result)


@bp.route('/companies/<c_id>', methods=['DELETE'])
@login_required
def delete_company(c_id):
    """Delete specified company and their admin
    """

    result = Company.delete_object(c_id)
    setattr(g, 'result', result)

    return result


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


@bp.route('/users/<u_id>', methods=['GET'])
@login_required
def read_user(u_id):
    """Return specified user
    """

    result = User.get_object(id=u_id)
    setattr(g, 'result', result)

    return result


@bp.route('/users/<u_id>', methods=['POST'])
@login_required
def update_user(u_id):
    """Update an API admin user
    """

    data = request.get_json()
    u = User.objects.get(id=u_id)

    password = data['password']
    u.set_name(data['name'])
    u.set_email(data['email'])
    u.set_password(User.encrypt(data['password']))

    result = User.save_object(u, password, mail=False)
    setattr(g, 'result', result)

    return result


@bp.route('/users/<u_id>', methods=['DELETE'])
@login_required
def delete_user(u_id):
    """Delete specified user
    """

    result = User.delete_object(u_id)
    setattr(g, 'result', result)

    return result


@bp.route('/logs', methods=['GET'])
@login_required
def logs():
    """Get all the logs
    """

    result = Log.get_all()
    setattr(g, 'result', result)

    return render_template('logs.html', logs=result)


@bp.route('/', methods=['GET'])
def index():
    """Show API Admin Index
    """

    setattr(g, 'result', 'index')

    if current_user.is_authenticated():
        return redirect('/admin/companies')
    else:
        return render_template('login.html')