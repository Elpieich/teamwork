# -*- encoding:utf-8 -*-

from crm.core import db


class Permission(db.Document):
    name = db.StringField(required=True)
    description = db.StringField(required=True)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, desc):
        self.description = desc