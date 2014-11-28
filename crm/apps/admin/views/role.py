# -*- coding: utf-8 -*-
"""
    crm.admin.views.role
    ----------------

    crm panel admin role views
"""

import json

from flask import request, render_template, g, Blueprint
from flask_security.core import current_user

from crm.models_admin.permission import Permission
from crm.models_admin.role import Role
from ..helpers import login_required, save_activity


bp = Blueprint('role', __name__, template_folder='templates')


@bp.after_request
def check_response(response):
    """Save in the activity log the request result
    """
    return save_activity(response)


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


@bp.route('/roles/<role_id>', methods=['GET'])
@login_required
def read_role(role_id):
    """Return specified role
    """
    result = Role.get_object(id=role_id)
    setattr(g, 'result', result)
    return result


@bp.route('/roles/<role_id>', methods=['POST'])
@login_required
def update_role(role_id):
    """Update specified role
    """
    data = request.get_json()
    r = Role.objects.get(id=role_id)
    # r.set_name(data['name'])
    r.set_description(data['description'])
    perms = json.loads(data['permissions'])
    result = Role.save_object(r, perms)
    setattr(g, 'result', result)
    return result


@bp.route('/roles/<role_id>', methods=['DELETE'])
@login_required
def delete_role(role_id):
    """Delete specified permission
    """
    result = Role.delete_object(role_id)
    setattr(g, 'result', result)
    return result
