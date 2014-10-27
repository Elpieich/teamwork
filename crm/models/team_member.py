# -*- encoding:utf-8 -*-

from ..core import db
from . import User


class Member(User, db.EmbeddedDocument):

    def register_sale(self, sale):
        pass

    def complete_task(self, task):
        pass
