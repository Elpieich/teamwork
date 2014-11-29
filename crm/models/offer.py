# -*- encoding:utf-8 -*-

from ..core import db
from crm.helpers import get_user_by_token

class Offer(db.Document):
    items = db.ListField(db.ReferenceField('Item'))
    discount = db.FloatField()
    start_date = db.DateTimeField(default=datetime.datetime.now)
    end_date = db.DateTimeField()
    accepted = db.BooleanField(default=False)
    comments = db.StringField(max_length=255)
    company = db.ReferenceField('Company')

    def save(self, *args, **kwargs):
        token = kwargs['auth_token']
        user = get_user_by_token(token)
        self.company = user.company
        return super(Offer, self).save(*args, **kwargs)

    def get_id(self):
        return self.id

    def get_items(self):
        return self.items

    def set_items(self, items):
        self.items = items

    def set_item(self, index, item):
        self.items.insert(index, item)

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def has_item(self, item):
        return item in self.items

    def get_discount(self):
        return self.discount

    def set_discount(self, discount):
        self.discount = discount

    def get_start_date(self):
        return self.start_date

    def set_start_date(self, date):
        self.start_date = date

    def get_end_date(self):
        return self.end_date

    def set_end_date(self, date):
        self.end_date = date

    def get_total(self):
        return sum([price for item.price in self.items])
