# -*- coding: utf-8 -*-
"""
    crm.api
    -------

    crm api application package
"""

from functools import wraps

from flask import jsonify
from flask_security import login_required

from flask_security import MongoEngineUserDatastore
from crm.core import db, security
from crm.models import User, Role
from crm.factory import Factory
from crm.helpers import JSONEncoder


class API:

    def __init__(self, settings_override=None):
        """Returns the CRM API application instance"""

        self.__app__ = Factory.create_app(
            __name__,
            __path__,
            settings_override)

        # Set the default JSON encoder
        self.__app__.json_encoder = JSONEncoder

        # Register custom error handlers
        #app.errorhandler(OverholtError)(on_overholt_error)
        #app.errorhandler(OverholtFormError)(on_overholt_form_error)
        self.__app__.errorhandler(404)(on_404)

        user_datastore = MongoEngineUserDatastore(db, User, Role)
        security.init_app(
            self.__app__,
            user_datastore,
            register_blueprint=False)

    def get_app(self):
        return self.__app__


    @staticmethod
    def route(bp, *args, **kwargs):
        kwargs.setdefault('strict_slashes', False)

        def decorator(f):
            @bp.route(*args, **kwargs)
            #@login_required
            @wraps(f)
            def wrapper(*args, **kwargs):
                sc = 200
                rv = f(*args, **kwargs)
                if isinstance(rv, tuple):
                    sc = rv[1]
                    rv = rv[0]
                return jsonify(dict(data=rv)), sc
            return f

        return decorator



def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        #@login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return jsonify(dict(data=rv)), sc
        return f

    return decorator



def on_overholt_error(e):
    return jsonify(dict(error=e.msg)), 400


def on_overholt_form_error(e):
    return jsonify(dict(errors=e.errors)), 400


def on_404(e):
    return jsonify(dict(error='Not found')), 404




# encoding: utf-8
"""
errors.py

Created by grevych on 2014-07-25.
Copyright (c) 2014 __MyCompanyName__. All rights reserved.
"""

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