# -*- coding: utf-8 -*-
"""
    crm.api
    -------

    crm api application package
"""

from functools import wraps
from bson import json_util

from flask import request
from flask_security import MongoEngineUserDatastore
from flask_security.decorators import _check_token

from crm.core import db, security
from crm.models import User, Role
from crm.factory import Factory
from crm.helpers import JSONEncoder
from crm.middlewares import HTTPMethodOverrideMiddleware


class API:
    content_types = ('application/json', )
    methods = ('GET', 'POST', 'PUT', 'DELETE', 'UPDATE', )

    def __init__(self, settings_override=None):
        """Returns the CRM API application instance"""
        self.app = Factory.create_app(
            __name__,
            __path__,
            settings_override)
        db.init_app(self.app)
        security.init_app(
            self.app,
            MongoEngineUserDatastore(db, User, Role),
            register_blueprint=False)
        self.app.json_encoder = JSONEncoder
        self.app.wsgi_app = HTTPMethodOverrideMiddleware(self.app.wsgi_app)
        self.app.content_types = self.content_types
        self.app.methods = self.methods
        self.app.get_parameters = self.get_parameters
        self.app.authenticated = self.authenticated
        self.app.unauthorized = self.unauthorized
        self.app.output_format = output_format
        self.app.after_request(after_request)
        # Register custom error handlers
        # app.errorhandler(OverholtError)(on_overholt_error)
        # app.errorhandler(OverholtFormError)(on_overholt_form_error)
        # app.errorhandler(404)(on_404)

    @classmethod
    def get_parameters(cls, request):
        if set(cls.methods) & set([request.method]):
            return request.get_json()
        return None

    @staticmethod
    def authenticated():
        return _check_token()

    @staticmethod
    def unauthorized():
        pass
        # werkzeug.exceptions.Unauthorized


def output_format(response):
    print response
    if hasattr(response, 'to_json'):
        response = response.to_json()
    else:
        response = json_util.dumps(response)
    print response
    return response

def after_request(response):
    response.content_type = 'application/json'
    response.data = (response.status, response.data, ) [response.status_code == 200] 
    response.data = {
        'status': response.status_code,
        'version': 1,
        'uri':request.url,
        'data':response.data
    }
    return response


        #     rv = fn(*args, **kwargs)

        #     if hasattr(rv, 'to_json'):
        #         rv = rv.to_json()
        #     else:
        #         rv = json_util.dumps(rv)

        # # except db.DoesNotExist:
        # #     raise werkzeug.exceptions.ImATeapot
        # # except db.ValidationError:
        # #     raise werkzeug.exceptions.ImATeapot

        # if isinstance(rv, tuple):
        #     sc = rv[1]
        #     rv = rv[0]
        # return rv, sc


