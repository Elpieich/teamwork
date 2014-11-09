# -*- coding: utf-8 -*-
"""
    crm.services.offer
    ~~~~~~~~~~~~~~~~~~~~

    crm offer service
"""

from flask import jsonify, current_app

from ..service import Service
from ..models import Offer


class OfferService(Service):
    __model__ = Offer

    def __init__(self, *args, **kwargs):
        super(OfferService, self).__init__(*args, **kwargs)
        #self.categories = CategoryService()


    def _preprocess_params(self, **kwargs):
        return kwargs
    #     kwargs = super(ProcessService, self)._preprocess_params(kwargs)
    #     categories = kwargs.get('categories', [])
    #     if categories and all(isinstance(c, int) for c in categories):
    #         kwargs['categories'] = self.categories.get_all(*categories)
    #     return kwargs