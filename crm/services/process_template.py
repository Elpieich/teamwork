# -*- coding: utf-8 -*-
"""
    crm.services.process
    ~~~~~~~~~~~~~~~~~~~~

    crm proceses service
"""

from flask import jsonify, current_app

from ..service import Service
from ..models import ProcessTemplate


class ProcessTemplateService(Service):
    __model__ = ProcessTemplate

    def __init__(self, *args, **kwargs):
        super(ProcessTemplateService, self).__init__(*args, **kwargs)
        #self.categories = CategoryService()


    def _preprocess_params(self, **kwargs):
        return kwargs
    #     kwargs = super(ProcessService, self)._preprocess_params(kwargs)
    #     categories = kwargs.get('categories', [])
    #     if categories and all(isinstance(c, int) for c in categories):
    #         kwargs['categories'] = self.categories.get_all(*categories)
    #     return kwargs