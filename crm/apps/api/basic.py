# -*- coding: utf-8 -*-
"""
    crm.api.basic
    ----------------

    Basic endpoints
"""

from flask import Blueprint, request

from crm.services import user
from crm.service import route

bp = Blueprint('basic', __name__)


#
#    USERS
#   -------
#
@route(bp, '/users')
def users():
    """
    """
    service = user()
    return service.all()

@route(bp, '/users', methods=['POST'])
def user_create():
    """
    """
    service = user()
    return service.create()

@route(bp, '/users/<user_id>')
def user_detail(user_id):
    """
    """
    service = user()
    return service.get(user_id)

@route(bp, '/users/<user_id>', methods=['PUT'])
def user_update(user_id):
    """
    """
    service = user()
    return service.update(user_id)

@route(bp, '/users/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    """
    """
    service = user()
    return service.delete(user_id)

@route(bp, '/users/search')
def users_search():
    """
    """
    service = user()
    return service.find()
