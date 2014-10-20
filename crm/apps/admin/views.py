# -*- coding: utf-8 -*-
"""
    crm.admin.views
    ----------------

    Admin controllers
"""

from flask import Blueprint, request, render_template
import json

from crm.models.permission import Permission
from crm.models.role import Role
from crm.models.company import Company
from crm.models.admin import Admin
from crm.models.user import User

bp = Blueprint('admin', __name__)


@bp.route('/permissions', methods=['GET'])
def permissions():
    """
    Return a list with all the system permissions
    """

    p = Permission.objects()

    return render_template('permissions.html', permissions=p)


@bp.route('/permissions', methods=['POST'])
def create_permissions():
    """
    Create a new permission
    """

    data = request.get_json()
    p = Permission()

    p.set_name(data['name'])
    p.set_description(data['description'])
    p.save()

    return p.to_json()


@bp.route('/permissions/<p_id>', methods=['GET'])
def read_permission(p_id):
    """
    Return specified permission
    """

    p = Permission.objects.get(id=p_id)

    return p.to_json()


@bp.route('/permissions/<p_id>', methods=['POST'])
def update_permission(p_id):
    """
    Update specified permission
    """

    data = request.get_json()
    p = Permission.objects.get(id=p_id)

    p.set_name(data['name'])
    p.set_description(data['description'])
    p.save()

    return 'Updated'


@bp.route('/permissions/<p_id>', methods=['DELETE'])
def delete_permission(p_id):
    """
    Delete specified permission
    """

    Permission.objects.get(id=p_id).delete()

    return 'Deleted'


@bp.route('/roles', methods=['GET'])
def roles():
    """
    Return a list with all the system roles
    """

    r = Role.objects()
    p = Permission.objects()

    return render_template('roles.html', roles=r, permissions=p)


@bp.route('/roles', methods=['POST'])
def create_role():
    """
    Create a new role

    """

    data = request.get_json()
    r = Role()

    r.set_name(data['name'])
    r.set_description(data['description'])
    perms = json.loads(data['permissions'])
    r.save() # First save the role after add permissions
    r.add_permissions(perms)

    return r.to_json()


@bp.route('/roles/<r_id>', methods=['GET'])
def read_role(r_id):
    """
    Return specified role
    """

    r = Role.objects.get(id=r_id)

    return r.to_json()


@bp.route('/roles/<r_id>', methods=['POST'])
def update_role(r_id):
    """
    Update specified role
    """

    data = request.get_json()
    r = Role.objects.get(id=r_id)

    r.set_name(data['name'])
    r.set_description(data['description'])
    perms = json.loads(data['permissions'])
    r.save()
    r.add_permissions(perms)

    return 'Updated'


@bp.route('/roles/<r_id>', methods=['DELETE'])
def delete_role(r_id):
    """
    Delete specified permission
    """

    Role.objects.get(id=r_id).delete()

    return 'Deleted'


@bp.route('/', methods=['GET']) # TODO: make login function
@bp.route('/companies', methods=['GET'])
def companies():
    """
    Return a list with all the system companies
    """

    c = Company.objects()

    return render_template('companies.html', companies=c)


@bp.route('/companies', methods=['POST'])
def create_company():
    """
    Create a new company
    """

    data = request.get_json()
    c = Company()
    admin = Admin()

    c.set_name(data['name'])
    c.set_direction(data['direction'])

    admin.set_name(data['admin_name'])
    admin.set_email(data['admin_email'])
    admin.set_role(
        Role.objects.get(name='Company administrator')
    )
    admin.save(validate=False) # TODO: revisar validaciones

    c.set_admin(admin)
    c.save()

    return c.to_json()

@bp.route('/companies/<c_id>', methods=['GET'])
def read_company(c_id):
    """
    Return specified company
    """

    c = Company.objects.get(id=c_id)

    dictionary = {
        'name': c.get_name(),
        'direction': c.get_direction(),
        'admin-name': c.get_admin().get_name(),
        'admin-email': c.get_admin().get_email()
    }

    return  json.dumps(dictionary)


@bp.route('/companies/<c_id>', methods=['POST'])
def update_company(c_id):
    """
    Update specified company and their administrator
    """

    data = request.get_json()
    c = Company.objects.get(id=c_id)

    c.get_admin().set_name(data['admin_name'])
    c.get_admin().set_email(data['admin_email'])
    c.get_admin().save(validate=False) # TODO: revisar validaciones
    c.set_name(data['name'])
    c.set_direction(data['direction'])
    c.save()

    dictionary = {
        'name': c.get_name(),
        'direction': c.get_direction(),
        'admin-name': c.get_admin().get_name(),
        'admin-email': c.get_admin().get_email()
    }

    return json.dumps(dictionary)


@bp.route('/companies/<c_id>', methods=['DELETE'])
def delete_company(c_id):
    """
    Delete specified company and their admin
    """

    c = Company.objects.get(id=c_id)
    Admin.objects.get(id=c.get_admin().id).delete()
    c.delete()

    return 'Deleted'

@bp.route('/users', methods=['GET'])
def users():
    """
    Get all API Admin users
    :return:
    """

    u = User.objects(
        role = Role.objects.get(name='Administrator API panel')
    )

    return render_template('users.html', users=u)


@bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new API admin user

    """
    data = request.get_json()
    u = User()

    u.set_name(data['name'])
    u.set_email(data['email'])
    u.set_password(data['password'])
    u.set_role(Role.objects.get(name='Administrator API panel'))
    u.save(validate=False)

    return u.to_json()


@bp.route('/users/<u_id>', methods=['GET'])
def read_user(u_id):
    """
    Return specified user
    """

    u = User.objects.get(id=u_id)

    return  u.to_json()


@bp.route('/users/<u_id>', methods=['POST'])
def update_user(u_id):
    """
    Update an API admin user

    """
    data = request.get_json()
    u = User.objects.get(id=u_id)

    u.set_name(data['name'])
    u.set_email(data['email'])
    u.set_password(data['password'])
    u.save(validate=False)

    return u.to_json()


@bp.route('/users/<u_id>', methods=['DELETE'])
def delete_user(u_id):
    """
    Delete specified user
    """

    User.objects.get(id=u_id).delete()

    return 'Deleted'