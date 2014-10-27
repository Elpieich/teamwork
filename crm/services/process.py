# -*- coding: utf-8 -*-
"""
    crm.services.process
    ~~~~~~~~~~~~~~~~~~~~

    crm proceses service
"""

from flask import jsonify, current_app

from ..service import Service
from ..models import Process


class ProcessService(Service):
    __model__ = Process

    def __init__(self, *args, **kwargs):
        super(ProcessService, self).__init__(*args, **kwargs)

    def _preprocess_params(self, **kwargs):
        return kwargs

    def get_stages(self, id):
        return self.__model__.objects.get(id=id).get_stages()

