# -*- encoding:utf-8 -*-

from ..core import db
from . import User


class Admin(User):

    teams = db.ListField(db.ReferenceField('Team'))

    def get_auth_token(self):
        return super(Admin, self).get_auth_token()