# -*- coding: utf-8 -*-
"""
    crm.services.item
    ~~~~~~~~~~~~~~~~~~~~

    crm item service
"""

from flask import jsonify, current_app

from ..service import Service
from ..models import Item


class ItemService(Service):
    __model__ = Item

    def __init__(self, *args, **kwargs):
        super(ItemService, self).__init__(*args, **kwargs)
        #self.categories = CategoryService()


    def _preprocess_params(self, **kwargs):
        return kwargs
    #     kwargs = super(ProcessService, self)._preprocess_params(kwargs)
    #     categories = kwargs.get('categories', [])
    #     if categories and all(isinstance(c, int) for c in categories):
    #         kwargs['categories'] = self.categories.get_all(*categories)
    #     return kwargs