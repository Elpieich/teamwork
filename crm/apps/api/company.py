# -*- coding: utf-8 -*-
"""
    crm.api.company
    ----------------

    Company endpoints
"""

from flask import Blueprint, request

# from crm.services import company, item, offer, team, user
from crm.service import route


bp = Blueprint('company', __name__)


#
#    COMPANIES
#   -----------
#
@route(bp, '/companies')
def companies():
    """
    """
    service = company()
    return service.all()

@route(bp, '/companies', methods=['POST'])
def company_create():
    """
    """
    service = company()
    return service.create()

@route(bp, '/companies/<company_id>')
def company_detail(company_id):
    """
    """
    service = company()
    return service.get(company_id)

@route(bp, '/companies/<company_id>/all')
def company_detail(company_id):
    """
    """
    service = company()
    return service.get(company_id, full=True)

@route(bp, '/companies/<company_id>/members')
def company_detail(company_id):
    """
    """
    service = company()
    return service.get(company_id, field='members')

@route(bp, '/companies/<company_id>/teams')
def company_detail(company_id):
    """
    """
    service = company()
    return service.get(company_id, field='teams')

@route(bp, '/companies/<company_id>/items')
def company_detail(company_id):
    """
    """
    service = company()
    return service.get(company_id, field='items')

@route(bp, '/companies/<company_id>/processes')
def company_detail(company_id):
    """
    """
    service = company()
    return service.get(company_id, field='processes')

@route(bp, '/companies/<company_id>', methods=['UPDATE'])
def company_update(company_id):
    """
    """
    service = company()
    return service.update(company_id)

@route(bp, '/companies/<company_id>', methods=['DELETE'])
def company_delete(company_id):
    """
    """
    service = company()
    return service.delete(company_id)

@route(bp, '/companies/search')
def companies_search():
    """
    """
    service = company()
    return service.find()


#
#    MEMBERS
#   ---------
#
@route(bp, '/members')
def members():
    """
    """
    service = member()
    return service.all()

@route(bp, '/members', methods=['POST'])
def member_create():
    """
    """
    service = member()
    return service.create()

@route(bp, '/members/<member_id>')
def member_detail(member_id):
    """
    """
    service = member()
    return service.get(member_id)

@route(bp, '/members/<member_id>', methods=['PUT'])
def member_update(member_id):
    """
    """
    service = member()
    return service.update(member_id)

@route(bp, '/members/<member_id>', methods=['DELETE'])
def member_delete(member_id):
    """
    """
    service = member()
    return service.delete(member_id)

@route(bp, '/members/search')
def members_search():
    """
    """
    service = member()
    return service.find()

#
#    ITEMS
#   -------
#
@route(bp, '/items')
def items():
    """
    """
    service = item()
    return service.all()

@route(bp, '/items', methods=['POST'])
def item_create():
    """
    """
    service = item()
    return service.create()

@route(bp, '/items/<item_id>')
def item_detail(item_id):
    """
    """
    service = item()
    return service.get(item_id)

@route(bp, '/items/<item_id>', methods=['PUT'])
def item_update(item_id):
    """
    """
    service = item()
    return service.update(item_id)

@route(bp, '/item/<item_id>', methods=['DELETE'])
def item_delete(item_id):
    """
    """
    service = item()
    return service.delete(item_id)

@route(bp, '/items/search')
def items_search():
    """
    """
    service = item()
    return service.find()
