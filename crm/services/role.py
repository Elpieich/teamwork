# -*- coding: utf-8 -*-
"""
    crm.services.role
    ~~~~~~~~~~~~~~~~~~~~

    crm role service
"""

from flask import jsonify, current_app

from ..service import Service
from ..models import Role


class RoleService(Service):
    __model__ = Role

    def __init__(self, *args, **kwargs):
        super(RoleService, self).__init__(*args, **kwargs)
        #self.categories = CategoryService()


    def _preprocess_params(self, **kwargs):
        return kwargs
    #     kwargs = super(ProcessService, self)._preprocess_params(kwargs)
    #     categories = kwargs.get('categories', [])
    #     if categories and all(isinstance(c, int) for c in categories):
    #         kwargs['categories'] = self.categories.get_all(*categories)
    #     return kwargs