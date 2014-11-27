# -*- coding: utf-8 -*-
"""
    crm.admin
    -------

    crm panel admin package
"""

from flask import render_template
from flask_security import MongoEngineUserDatastore
from flask_security.core import current_user

from crm.core import db, toolbar, mail, security
from crm.models import User, Role
from crm.factory import Factory
from crm.helpers import JSONEncoder


class Admin:
    content_types = ('application/json', )
    methods = ('GET', 'POST', 'PUT', 'DELETE', )

    def __init__(self, settings_override=None):
        """Returns the API panel application instance"""
        self.app = Factory.create_app(
            __name__,
            __path__,
            settings_override)
        db.init_app(self.app)
        toolbar.init_app(self.app)
        mail.init_app(self.app)
        security.init_app(
            self.app,
            MongoEngineUserDatastore(db, User, Role),
            register_blueprint=False)
        self.app.json_encoder = JSONEncoder
        self.app.content_types = self.content_types
        self.app.methods = self.methods


    @classmethod
    def get_parameters(cls, request):
        if set(cls.methods) & set([request.method]):
            return request.get_json()
        return None

    @staticmethod
    def authenticated():
        return current_user.is_authenticated()

    @staticmethod
    def unauthorized():
        """Return a message to the unauthorized user
        """
        errors = "The server could not verify that you are authorized to access the URL requested." \
                 " You either supplied the wrong credentials (e.g. a bad password), " \
                 "or your browser doesn't understand how to supply the credentials required."
        return render_template('login.html', errors=errors)
