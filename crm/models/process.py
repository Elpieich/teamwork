# -*- encoding:utf-8 -*-

from crm.core import db


STATUS = (
    'Abierta',
    'En espera',
    'Cancelada',
    'Cerrada')


class Process(db.Document):
    name = db.StringField(
        max_length=40,
        required=True)
    description = db.StringField(
        max_length=140,
        required=True)
    template = db.ReferenceField('ProcessTemplate')
    #team = db.ReferenceField('Team')
    #manager = db.ReferenceField('User')
    status = db.ReferenceField('ProcessStatus')
    stages = db.ListField(
        db.ReferenceField('Stage'))
    parent = db.ReferenceField('Process')
    variables = db.ListField()

    def get_id(self):
        return self.__id__

    def set_id(self, id):
        self.__id__ = id

    def get_process(self):
        return self.__process__

    def set_process(self, process):
        self.__process__ = process

    def add_offer(self, offer):
        pass

    def remove_offer(self, offer):
        pass

    def get_offers(self):
        return self.__offers__

    def get_latest_offer(self):
        pass

    def get_status(self):
        return self.__status__

    def get_customer(self):
        return self.__customer__

    def set_customer(self, customer):
        self.__customer__ = customer
