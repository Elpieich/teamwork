# -*- coding: utf-8 -*-
"""
    crm.services.company
    ~~~~~~~~~~~~~~~~~~~~

    crm company service
"""

from flask import jsonify, current_app

from ..service import Service
from ..models import Company


class CompanyService(Service):
    __model__ = Company

    def __init__(self, *args, **kwargs):
        super(CompanyService, self).__init__(*args, **kwargs)
        #self.categories = CategoryService()


    def _preprocess_params(self, **kwargs):
        return kwargs
    #     kwargs = super(ProcessService, self)._preprocess_params(kwargs)
    #     categories = kwargs.get('categories', [])
    #     if categories and all(isinstance(c, int) for c in categories):
    #         kwargs['categories'] = self.categories.get_all(*categories)
    #     return kwargs