# -*- coding: utf-8 -*-
"""
    crm.admin
    -------

    crm api panel admin package
"""

from functools import wraps

from flask import jsonify, Flask

from crm.core import db, security, user_datastore
from crm.models import User, Role
from crm.factory import Factory
from crm.helpers import JSONEncoder

app = Flask(__name__)

class Admin:

    def __init__(self, settings_override=None):
        """Returns the API panel application instance"""

        self.__app__ = Factory.create_app(
            __name__,
            __path__,
            settings_override)

        # Set the default JSON encoder
        self.__app__.json_encoder = JSONEncoder
        self.__app__.security = None

        # Register custom error handlers
        #app.errorhandler(OverholtError)(on_overholt_error)
        #app.errorhandler(OverholtFormError)(on_overholt_form_error)
        self.__app__.errorhandler(404)(on_404)

        security.init_app(
            self.__app__,
            user_datastore(db, User, Role),
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
                return rv, sc
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
            return rv, sc
        return f

    return decorator


def on_overholt_error(e):
    return jsonify(dict(error=e.msg)), 400


def on_overholt_form_error(e):
    return jsonify(dict(errors=e.errors)), 400


def on_404(e):
    return jsonify(dict(error='Not found')), 404