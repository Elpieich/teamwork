# -*- coding: utf-8 -*-
"""
    crm.process
    ~~~~~~~~~~~~~~~~~

    crm proceses service
"""

from flask import jsonify, current_app

from ..services import Service
from ..models import Process


# class CategoryService(Service):
#     __model__ = Categorys

class ProcessService(Service):
    __model__ = Process

    def __init__(self, *args, **kwargs):
        super(ProcessService, self).__init__(*args, **kwargs)
        # self.categories = CategoryService()

    def all(self):
        return self.__model__.objects()

    #def _preprocess_params(self, kwargs):
        #pass
        # kwargs = super(ProcessService, self)._preprocess_params(kwargs)
        # categories = kwargs.get('categories', [])
        # if categories and all(isinstance(c, int) for c in categories):
        #     kwargs['categories'] = self.categories.get_all(*categories)
        # return kwargs