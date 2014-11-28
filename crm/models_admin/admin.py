# -*- encoding:utf-8 -*-

from .user import User
from crm.core import db
from crm.models.team import Team


class Admin(User):

    teams = db.ListField(db.ReferenceField(Team))

    def get_auth_token(self):
        return super(Admin, self).get_auth_token()