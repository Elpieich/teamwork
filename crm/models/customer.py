# -*- encoding:utf-8 -*-

from ..core import db


class Customer(db.Document):
    processes = db.ListField(db.ReferenceField('Process'))

    def reply_offer(self):
        pass
