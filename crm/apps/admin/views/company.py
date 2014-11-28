# -*- coding: utf-8 -*-
"""
    crm.admin.views.company
    ----------------

    crm panel admin company views
"""

import json

from flask import request, render_template, g, Blueprint
from flask_security.core import current_user

from crm.models_admin.role import Role
from crm.models_admin.company import Company
from crm.models_admin.admin import Admin
from crm.models_admin.user import User
from ..helpers import login_required, save_activity


bp = Blueprint('company', __name__, template_folder='templates')


@bp.after_request
def check_response(response):
    """Save in the activity log the request result
    """
    return save_activity(response)


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


@bp.route('/companies/<company_id>', methods=['GET'])
@login_required
def read_company(company_id):
    """Return specified company
    """
    result = Company.get_object(id=company_id)
    setattr(g, 'result', result)
    return result


@bp.route('/companies/<company_id>', methods=['POST'])
@login_required
def update_company(company_id):
    """Update specified company and their administrator
    """
    data = request.get_json()
    compa = Company.objects.get(id=company_id)
    admin = compa.get_admin()
    compa.set_name(data['name'])
    compa.set_direction(data['direction'])
    admin.set_name(data['admin_name'])
    admin.set_email(data['admin_email'])
    result = Company.save_object(compa, admin, None, edit=True)
    setattr(g, 'result', json.dumps(result))
    return json.dumps(result)


@bp.route('/companies/<company_id>', methods=['DELETE'])
@login_required
def delete_company(company_id):
    """Delete specified company and their admin
    """
    result = Company.delete_object(company_id)
    setattr(g, 'result', result)
    return result