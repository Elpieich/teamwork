# -*- coding: utf-8 -*-
"""
    crm.admin.views.permission
    ----------------

    crm panel admin permission views
"""

from flask import request, render_template, g, redirect, Blueprint
from flask_security.core import current_user

from crm.models_admin.permission import Permission
from ..helpers import login_required


bp = Blueprint('permission', __name__, template_folder='templates')


@bp.route('/', methods=['GET'])
def index():
    """Show API Admin Index
    """
    setattr(g, 'result', 'index')
    if current_user.is_authenticated():
        return redirect('/admin/companies')
    else:
        return render_template('login.html')


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


@bp.route('/permissions/<permission_id>', methods=['GET'])
@login_required
def read_permission(permission_id):
    """Return specified permission
    """
    result = Permission.get_object(permission_id)
    setattr(g, 'result', result)
    return result


@bp.route('/permissions/<permission_id>', methods=['POST'])
@login_required
def update_permission(permission_id):
    """Update specified permission
    """
    data = request.get_json()
    p = Permission.objects.get(id=permission_id)
    p.set_name(data['name'])
    p.set_description(data['description'])
    result = Permission.save_object(p)
    setattr(g, 'result', result)
    return result


@bp.route('/permissions/<permission_id>', methods=['DELETE'])
@login_required
def delete_permission(permission_id):
    """Delete specified permission
    """
    result = Permission.delete_object(permission_id)
    setattr(g, 'result', result)
    return result
