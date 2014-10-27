# -*- coding: utf-8 -*-
"""
    crm.services.customer
    ~~~~~~~~~~~~~~~~~~~~

    crm customer service
"""

from flask import jsonify, current_app

from ..service import Service
from ..models import Customer


class CustomerService(Service):
    __model__ = Customer

    def __init__(self, *args, **kwargs):
        super(CustomerService, self).__init__(*args, **kwargs)
        #self.categories = CategoryService()


    def _preprocess_params(self, **kwargs):
        return kwargs
    #     kwargs = super(ProcessService, self)._preprocess_params(kwargs)
    #     categories = kwargs.get('categories', [])
    #     if categories and all(isinstance(c, int) for c in categories):
    #         kwargs['categories'] = self.categories.get_all(*categories)
    #     return kwargs