# -*- encoding:utf-8 -*-

from ..core import db


class Offer(db.Document):
    items = db.ListField(db.ReferenceField('Item'))
    discount = db.FloatField()
    start_date = db.DateTimeField()
    end_date = db.DateTimeField()

    # def get_id(self):
    #     return self.__id__

    # def set_id(self, id):
    #     self.__id__ = id

    # def get_items(self):
    #     return self.__items__

    # def set_items(self, items):
    #     self.__items__ = items

    # def add_item(self, item):
    #     pass

    # def remove_item(self, item):
    #     pass

    # def get_discount(self):
    #     return self.__discount__

    # def set_discount(self, discount):
    #     self.__discount__ = discount

    # def get_start_date(self):
    #     return self.__start_date__

    # def set_start_date(self, date):
    #     self.__start_date__ = date

    # def get_end_date(self):
    #     return self.__end_date__

    # def set_end_date(self, date):
    #     self.__end_date__ = date

    # def calculate_price(self):
    #     pass
