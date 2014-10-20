# -*- encoding:utf-8 -*-

from crm.core import db
# from .sale import Sale
# from .team_member import TeamMember


class Team(db.Document):
    name = db.StringField()
    # team_members = db.ListReference(db.FieldReference(TeamMember))
    # team_leader = db.ReferenceField(TeamMember)
    # sales = db.ListReference(db.FieldReference(Sale))


    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def add_team_member(self):
        pass

    def remove_team_member(self):
        pass

    def get_team_members(self):
        return self.__team_members__

    def set_team_leader(self, team_leader):
        pass

    def get_team_leader(self):
        pass

    def remove_team_leader(self):
        pass

    def add_sale(self):
        pass

    def remove_sale(self):
        pass
