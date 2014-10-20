# -*- encoding:utf-8 -*-

from crm.core import db
from .admin import Admin


class Company(db.Document):
    name = db.StringField()
    direction = db.StringField()
    admin = db.ReferenceField(Admin)


    def get_name(self):
        return self.name


    def set_name(self, name):
        self.name = name


    def get_direction(self):
        return self.direction


    def set_direction(self, dir):
        self.direction = dir


    def get_admin(self):
        return self.admin


    def set_admin(self, admin):
        self.admin = admin