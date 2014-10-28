# -*- encoding:utf-8 -*-

from ..core import db


STATUS = (
    ('A', 'Abierta', ),
    ('B', 'En espera', ),
    ('C', 'Cancelada', ),
    ('D', 'Cerrada'), )


class Process(db.Document):
    name = db.StringField(
        max_length=40,
        required=True)
    description = db.StringField(
        max_length=140,
        required=True)
    template = db.ReferenceField('ProcessTemplate')
    team = db.ReferenceField('Team')
    manager = db.ReferenceField('User')
    status = db.StringField(choices=STATUS)
    stages = db.ListField(
        db.ReferenceField('Stage'))

    def get_id(self):
        return self.id

    def add_offer(self, offer):
        pass

    def remove_offer(self, offer):
        pass

    # def get_offers(self):
    #     return self.offers

    def get_latest_offer(self):
        pass

    def get_status(self):
        return self.status

    # def get_customer(self):
    #     return self.__customer__

    # def set_customer(self, customer):
    #     self.__customer__ = customer
