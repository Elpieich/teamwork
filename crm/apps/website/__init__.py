# -*- coding: utf-8 -*-
"""
    crm.website
    -------

    crm website application package
"""

from crm.factory import Factory


class Website:

    def __init__(
        self, 
        settings_override=None, 
        register_security_blueprint=False
    ):
        """Returns the CRM Website application instance"""
        
        self.__app__ = Factory.create_app(
            __name__,
            __path__,
            settings_override,
            register_security_blueprint=register_security_blueprint)


    def get_app(self):
        return self.__app__
        
# from functools import wraps

# from flask import render_template
# from flask_security import LoginForm
# from flask_security import  current_user, login_required, login_user

# from crm import core
# #from . import assets

# app = None

# def create_app(settings_override=None):
#     """Returns the Overholt dashboard application instance"""
#     global app
#     app = core.create_app(__name__, __path__, settings_override)

#     # Init assets
#     #assets.init_app(app)
    
#     # print dir(core.security)

#     # Register custom error handlers
#     if not app.debug:
#         for e in [500, 404]:
#             app.errorhandler(e)(handle_error)

#     return app


# def handle_error(e):
#     return render_template('errors/%s.html' % e), e


# def route(bp, *args, **kwargs):
#     def decorator(f):
#         @bp.route(*args, **kwargs)
#         @login_required
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             return f(*args, **kwargs)
#         return f

#     return decorator