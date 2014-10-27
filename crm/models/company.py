# -*- encoding:utf-8 -*-

from ..core import db


class Company(db.Document):
    name = db.StringField(required=True, min_length=1, max_length=140)
    direction = db.StringField(required=True, min_length=1, max_length=140)
    admin = db.ReferenceField('User')

    def get_id(self):
        return self.id
        
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def get_admin(self):
        return self.admin

    def set_admin(self, admin):
        self.admin = admin
