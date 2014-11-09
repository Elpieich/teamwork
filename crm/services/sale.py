# -*- coding: utf-8 -*-
"""
    crm.services.sale
    ~~~~~~~~~~~~~~~~~~~~

    crm sale service
"""

from flask import jsonify, current_app

from ..service import Service
from ..models import Sale


class SaleService(Service):
    __model__ = Sale

    def __init__(self, *args, **kwargs):
        super(SaleService, self).__init__(*args, **kwargs)

    def _preprocess_params(self, **kwargs):
        return kwargs
