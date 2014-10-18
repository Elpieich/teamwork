# -*- coding: utf-8 -*-
"""
    crm.admin.views
    ----------------

    Admin controllers
"""

from flask import Blueprint, request, render_template

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

    json = request.get_json()
    p = Permission()
    p.set_name(json['name'])
    p.set_description(json['description'])
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

    json = request.get_json()
    p = Permission.objects.get(id=p_id)
    p.set_name(json['name'])
    p.set_description(json['description'])
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

    json = request.get_json()
    r = Role()
    r.set_name(json['name'])
    r.set_description(json['description'])
    r.save()
    #Get permissions

    return r.to_json(),