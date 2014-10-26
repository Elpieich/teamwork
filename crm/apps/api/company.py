# -*- coding: utf-8 -*-
"""
    crm.api.company
    ----------------

    Company endpoints
"""

from flask import Blueprint, request

from crm.service import route

bp = Blueprint('company', __name__)

@route(bp, '/companies')
def list_companies():
    """Returns a list of companies instances."""
    #return users.all()
    return {'items': 'all'}


@route(bp, '/company', methods=['POST'])
def create_company():
    """Creates a new company. Returns the new company instance."""
    # form = NewCompanyForm()
    # if form.validate_on_submit():
    #     return products.create(**request.json)
    # raise OverholtFormError(form.errors)
    pass


@route(bp, '/company/<company_id>')
def detail_company(company_id):
    """Returns a company instance."""
    # return company.get_or_404(company_id)
    pass


@route(bp, '/company/<company_id>', methods=['PUT'])
def update_company(company_id):
    """Updates a company. Returns a company instance."""
    # form = UpdateProductForm()
    # if form.validate_on_submit():
    #     return company.update(company.get_or_404(company_id), **request.json)
    # raise(OverholtFormError(form.errors))
    pass


@route(bp, '/company/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    """Deletes a company. Returns a 204 response."""
    # company.delete(company.get_or_404(company_id))
    # return None, 204
    pass


@route(bp, '/items')
def list_items():
    """Returns a list of items instances."""
    #return items.all()
    return {'items': 'all'}


@route(bp, '/item', methods=['POST'])
def create_item():
    """Creates an new item. Returns the new item instance."""
    # form = NewCompanyForm()
    # if form.validate_on_submit():
    #     return products.create(**request.json)
    # raise OverholtFormError(form.errors)
    pass


@route(bp, '/item/<item_id>')
def detail_item(item_id):
    """Returns an item instance."""
    # return item.get_or_404(item_id)
    pass


@route(bp, '/item/<item_id>', methods=['PUT'])
def update_item(item_id):
    """Updates an item. Returns an item instance."""
    # form = UpdateProductForm()
    # if form.validate_on_submit():
    #     return item.update(item.get_or_404(item_id), **request.json)
    # raise(OverholtFormError(form.errors))
    pass


@route(bp, '/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Deletes an item. Returns a 204 response."""
    # item.delete(item.get_or_404(company_id))
    # return None, 204
    pass
