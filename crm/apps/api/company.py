# -*- coding: utf-8 -*-
"""
    crm.api.company
    ----------------

    Company endpoints
"""

from flask import Blueprint, request

from crm.services import company, item, offer, team, user
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
def company_detail_all(company_id):
    """
    """
    service = company()
    return service.get(company_id, full=True)

@route(bp, '/companies/<company_id>/<field>')
def company_detail_field(company_id, field):
    """
    """
    service = company()
    return service.get(company_id, field=field)

# @route(bp, '/companies/<company_id>/members')
# def company_detail(company_id):
#     """
#     """
#     service = company()
#     return service.get(company_id, field='members')

# @route(bp, '/companies/<company_id>/teams')
# def company_detail(company_id):
#     """
#     """
#     service = company()
#     return service.get(company_id, field='teams')

# @route(bp, '/companies/<company_id>/items')
# def company_detail(company_id):
#     """
#     """
#     service = company()
#     return service.get(company_id, field='items')

# @route(bp, '/companies/<company_id>/processes')
# def company_detail(company_id):
#     """
#     """
#     service = company()
#     return service.get(company_id, field='processes')

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
    service = user()
    return service.all()

@route(bp, '/members', methods=['POST'])
def member_create():
    """
    """
    service = user()
    return service.create()

@route(bp, '/members/<member_id>')
def member_detail(member_id):
    """
    """
    service = user()
    return service.get(member_id)

@route(bp, '/members/<member_id>', methods=['PUT'])
def member_update(member_id):
    """
    """
    service = user()
    return service.update(member_id)

@route(bp, '/members/<member_id>', methods=['DELETE'])
def member_delete(member_id):
    """
    """
    service = user()
    return service.delete(member_id)

@route(bp, '/members/search')
def members_search():
    """
    """
    service = user()
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


#
#    OFFERS
#   --------
#
@route(bp, '/offers')
def offers():
    """
    """
    service = offer()
    return service.all()

@route(bp, '/offers', methods=['POST'])
def offer_create():
    """
    """
    service = offer()
    return service.create()

@route(bp, '/offers/<offer_id>')
def offer_detail(offer_id):
    """
    """
    service = offer()
    return service.get(offer_id)

@route(bp, '/offers/<offer_id>', methods=['PUT'])
def offer_update(offer_id):
    """
    """
    service = offer()
    return service.update(offer_id)

@route(bp, '/offers/<offer_id>', methods=['DELETE'])
def offer_delete(offer_id):
    """
    """
    service = offer()
    return service.delete(offer_id)

@route(bp, '/offers/search')
def offers_search():
    """
    """
    service = offer()
    return service.find()


#
#    TEAMS
#   -------
#
@route(bp, '/teams')
def teams():
    """
    """
    service = team()
    return service.all()

@route(bp, '/teams', methods=['POST'])
def team_create():
    """
    """
    service = team()
    return service.create()

@route(bp, '/teams/<team_id>')
def team_detail(team_id):
    """
    """
    service = team()
    return service.get(team_id)

@route(bp, '/teams/<team_id>', methods=['PUT'])
def team_update(team_id):
    """
    """
    service = team()
    return service.update(team_id)

@route(bp, '/teams/<team_id>', methods=['DELETE'])
def team_delete(team_id):
    """
    """
    service = team()
    return service.delete(team_id)

@route(bp, '/teams/search')
def teams_search():
    """
    """
    service = team()
    return service.find()


#
#    SALES
#   -------
#
@route(bp, '/sales')
def sales():
    """
    """
    service = sale()
    return service.all()

@route(bp, '/sales', methods=['POST'])
def sale_create():
    """
    """
    service = sale()
    return service.create()

@route(bp, '/sales/<sale_id>')
def sale_detail(sale_id):
    """
    """
    service = sale()
    return service.get(sale_id)

@route(bp, '/sales/<sale_id>', methods=['PUT'])
def sale_update(sale_id):
    """
    """
    service = sale()
    return service.update(sale_id)

@route(bp, '/sales/<sale_id>', methods=['DELETE'])
def sale_delete(sale_id):
    """
    """
    service = sale()
    return service.delete(sale_id)

@route(bp, '/sales/search')
def sales_search():
    """
    """
    service = sale()
    return service.find()


#
#    CUSTOMERS
#   -----------
#
@route(bp, '/customers')
def customers():
    """
    """
    service = customer()
    return service.all()

@route(bp, '/customers', methods=['POST'])
def customer_create():
    """
    """
    service = customer()
    return service.create()

@route(bp, '/customers/<customer_id>')
def customer_detail(customer_id):
    """
    """
    service = customer()
    return service.get(customer_id)

@route(bp, '/customers/<customer_id>', methods=['PUT'])
def customer_update(customer_id):
    """
    """
    service = customer()
    return service.update(customer_id)

@route(bp, '/customers/<customer_id>', methods=['DELETE'])
def customer_delete(customer_id):
    """
    """
    service = customer()
    return service.delete(customer_id)

@route(bp, '/customers/search')
def customers_search():
    """
    """
    service = customer()
    return service.find()
