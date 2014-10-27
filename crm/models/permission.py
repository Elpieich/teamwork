# -*- encoding:utf-8 -*-

from ..core import db
import json


class Permission(db.Document):
    name = db.StringField(
        required=True,
        min_length=1,
        max_length=140)
    description = db.StringField(
        required=True,
        min_length=1,
        max_length=140)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, desc):
        self.description = desc

