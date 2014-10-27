# -*- encoding:utf-8 -*-

from ..core import db
from . import User

class Leader(User, db.EmbeddedDocument):

    def register_sale(self, sale):
        pass

    def complete_task(self, task):
        pass

    def assign_process(self):
        pass
