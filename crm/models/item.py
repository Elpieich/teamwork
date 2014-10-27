# -*- encoding:utf-8 -*-

from ..core import db


class Item(db.Document):
    name = db.StringField()
    description = db.StringField()
    price = db.FloatField()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price
