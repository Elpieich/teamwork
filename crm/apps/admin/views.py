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
    Create new permission
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
    Create new role

    """

    data = request.get_json()
    r = Role()
    r.set_name(data['name'])
    r.set_description(data['description'])
    permissions = json.loads(data['permissions'])
    r.save() # First save the role after add permissions
    r.add_permissions(permissions)

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
    permissions = json.loads(data['permissions'])
    r.save()
    r.add_permissions(permissions)

    return 'Updated'


@bp.route('/roles/<r_id>', methods=['DELETE'])
def delete_role(r_id):
    """
    Delete specified permission
    """

    Role.objects.get(id=r_id).delete()

    return 'Deleted'













