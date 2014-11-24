# -*- encoding:utf-8 -*-

from ..core import db
from . import Customer

STATUS = (
    ('A', 'Abierta', ),
    ('B', 'En espera', ),
    ('C', 'Cancelada', ),
    ('D', 'Cerrada'), )


class Sale(db.Document):
    customer = db.ReferenceField(Customer)
    owner = db.ReferenceField('Member')
    process = db.ReferenceField('Process')
    status = db.StringField(choices=STATUS)
    offers = db.ListField(db.ReferenceField('Offer'))
    team = db.ReferenceField('Team')

    def get_customer(self):
        return self.customer

    def set_customer(self, customer):
        self.customer = customer

    def get_process(self):
        return self.process

    def set_process(self, process):
        self.process = process

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_offers(self):
        return self.offers

    def set_offers(self, offers):
        for offer in self.offers:
            offer.delete()
        self.offers = offers

    def set_offer(self, index, offer):
        self.offers.insert(index, offer)

    def add_offer(self, offer):
        self.offers.append(offer)

    def remove_offer(self, offer):
        self.offers.remove(offer)

    def has_offer(self, offer):
        return offer in self.offers

    def get_last_offer(self):
        return self.offers[-1]

    def get_first_offer(self):
        return self.offers[0]
