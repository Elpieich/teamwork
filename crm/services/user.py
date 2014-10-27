# -*- coding: utf-8 -*-
"""
    crm.services.user
    ~~~~~~~~~~~~~~~~~~~~

    crm user service
"""

from flask import jsonify, current_app

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