# -*- coding: utf-8 -*-
"""
    crm.services.user
    ~~~~~~~~~~~~~~~~~

    crm user service
"""

from itertools import chain
from flask import jsonify, current_app
from flask_security.core import current_user
from flask_security.utils import get_hmac, verify_password


from ..service import Service
from ..models import User


class UserService(Service):
    __model__ = User

    def __init__(self, *args, **kwargs):
        super(UserService, self).__init__(*args, **kwargs)
        #self.categories = CategoryService()

    def _preprocess_params(self, **kwargs):
        return kwargs
    #     kwargs = super(ProcessService, self)._preprocess_params(kwargs)
    #     categories = kwargs.get('categories', [])
    #     if categories and all(isinstance(c, int) for c in categories):
    #         kwargs['categories'] = self.categories.get_all(*categories)
    #     return kwargs

    def create(self, **kwargs):
        """
        """
        parameters = dict(chain(self.__parameters__.items(), kwargs.items()))
        user = self.new(**parameters)
        if not user.get_password():
            return None
        hmac = get_hmac(user.get_password())
        user.set_password(hmac)
        return self.save(user)

    def authenticate(self):
        response = {}
        if not current_user.is_authenticated():
            if 'password' in self.__parameters__ and 'email' in self.__parameters__:
                user = self.__model__.objects.get(email=self.__parameters__['email'])
                if user and verify_password(self.__parameters__['password'], user.get_password()):
                    response['auth_token'] = user.get_auth_token()
                    response['roles'] = user.roles[0].get_name()
                    response['name'] = user.name
                    return response
            return current_app.unauthorized()
        response['auth_token'] = user.get_auth_token()
        response['roles'] = user.roles[0].get_name()
        response['name'] = user.name
        return response
