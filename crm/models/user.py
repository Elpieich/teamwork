# -*- encoding:utf-8 -*-

from flask_security.core import UserMixin
from ..core import db


class User(db.Document, UserMixin):
    name = db.StringField(required=True, min_length=4, max_length=140)
    password = db.StringField(required=True, min_length=8, max_length=50)
    token = db.StringField()
    email = db.EmailField(required=True, unique=True)
    roles = db.ListField(db.ReferenceField('Role'), default=[])
    company = db.ReferenceField('Company', required=True)
    active = db.BooleanField()
    meta = {'allow_inheritance': True}

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_company(self):
        return self.company

    def set_company(self, company):
        self.company = company

    def get_token(self):
        return self.token