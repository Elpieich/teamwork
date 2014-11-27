# -*- encoding:utf-8 -*-

from ..core import db
from crm.helpers import get_user_by_token


class Item(db.Document):
    name = db.StringField()
    description = db.StringField()
    price = db.FloatField(default=0.0)
    company = db.ReferenceField('Company')

    def save(self, *args, **kwargs):
        token = kwargs['auth_token']
        user = get_user_by_token(token)
        self.company = user.company
        return super(Item, self).save(*args, **kwargs)

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
