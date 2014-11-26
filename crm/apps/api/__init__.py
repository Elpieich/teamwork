# -*- coding: utf-8 -*-
"""
    crm.api
    -------

    crm api application package
"""

from functools import wraps
from bson import json_util

from flask_security import MongoEngineUserDatastore
from flask_security.decorators import _check_token

from crm.core import db, security
from crm.models import User, Role
from crm.factory import Factory
from crm.helpers import JSONEncoder
from crm.middlewares import HTTPMethodOverrideMiddleware


class API:
    conetnt_types = ('application/json', )
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

    @staticmethod
    def output_format(response):
        sc = 200
        if hasattr(response, 'to_json'):
                response = response.to_json()
        else:
                response = json_util.dumps(response)

        if isinstance(response, tuple):
            sc = response[1]
            response = response[0]
        return response, sc


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



# from flask import jsonify

# class InvalidUsage(Exception):
#     status_code = 400

#     def __init__(self, message, status_code=None, payload=None):
#         Exception.__init__(self)
#         self.message = message
#         if status_code is not None:
#             self.status_code = status_code
#         self.payload = payload

#     def to_dict(self):
#         rv = dict(self.payload or ())
#         rv['message'] = self.message
#         return rv
        
        
# @app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response
#     
#     
# @app.route('/foo')
# def get_foo():
#     raise InvalidUsage('This view is gone', status_code=410)