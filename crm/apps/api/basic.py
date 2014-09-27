# -*- coding: utf-8 -*-
"""
    crm.api.
    ----------------


"""

from flask import Blueprint, request

from . import route

bp = Blueprint('basic', __name__)

@route(bp, '/users')
def list_users():
    """Returns a list of users instances."""
    #return users.all()
    return {'users': 'all'}


@route(bp, '/user', methods=['POST'])
def create_user():
    """Creates a new user. Returns the new user instance."""
    # form = NewUserForm()
    # if form.validate_on_submit():
    #     return products.create(**request.json)
    # raise OverholtFormError(form.errors)
    pass


@route(bp, '/user/<user_id>')
def detail_user(user_id):
    """Returns a user instance."""
    # return products.get_or_404(user_id)
    pass


@route(bp, '/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a user. Returns the user process instance."""
    # form = UpdateProductForm()
    # if form.validate_on_submit():
    #     return products.update(products.get_or_404(product_id), **request.json)
    # raise(OverholtFormError(form.errors))
    pass


@route(bp, '/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user. Returns a 204 response."""
    # products.delete(products.get_or_404(user_id))
    # return None, 204
    pass