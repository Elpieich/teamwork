# -*- encoding:utf-8 -*-

from crm.core import db
from .user import User
from .team import Team


class Admin(User):

    teams = db.ListField(db.ReferenceField(Team))

    def add_team(self, team):
        pass

    def remove_team(self, team):
        pass

    def get_teams(self):
        return self.teams

    def get_all_sales_status(self):
        pass

    def get_team_status(self, team):
        pass

    def get_auth_token(self):
        return super(Admin, self).get_auth_token()