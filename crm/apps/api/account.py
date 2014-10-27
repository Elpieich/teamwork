# -*- coding: utf-8 -*-
"""
    crm.api.account
    ----------------

    Account endpoints
"""

from flask import Blueprint, request

# from crm.services import user
# from crm.service import route


# bp = Blueprint('account', __name__, url_prefix='/account')


# @route(bp, '/')
# def account():
#     """Regresa una lista de cuentas de toda la
#     empresa
#     """
#     service = user()
#     return service.all()

# @route(bp, '/', methods=['POST'])
# def account_create():
#     """Crea una nueva cuenta para la empresa
#     """
#     service = user()
#     return service.create()

# @route(bp, '/<account_id>')
# def account_profile(account_id):
#     """Regresa el perfil de un usuario
#     """
#     service = user()
#     return service.get(account_id)

# @route(bp, '/<account_id>', methods=['UPDATE'])
# def account_update(account_id):
#     """Actualiza una cuenta de una empresa
#     """
#     service = user()
#     return service.update(account_id)

# @route(bp, '/<account_id>', methods=['DELETE'])
# def account_delete(account_id):
#     """Elimina una cuenta de una empresa
#     """
#     service = user()
#     return service.delete(account_id)

# @route(bp, '/<account_id>/settings')
# def account_settings(account_id):
#     """Regresa los ajustes de una cuenta
#     """
#     service = user()
#     return service.get(account_id, full=True)
