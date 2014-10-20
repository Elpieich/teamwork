# -*- encoding:utf-8 -*-

from crm.core import db
from .role import Role

class User(db.Document):
    name = db.StringField()
    email = db.EmailField()
    role = db.ReferenceField(Role)
    password = db.StringField()

    meta = {'allow_inheritance': True}


    def get_name(self):
        return self.name


    def set_name(self, name):
        self.name = name


    def get_email(self):
        return self.email


    def set_email(self, email):
        self.email = email


    def get_role(self):
        return self.role


    def set_role(self, role):
        self.role = role

    def get_password(self):
        return self.password

    def set_password(self, passw):
        self.password = passw

