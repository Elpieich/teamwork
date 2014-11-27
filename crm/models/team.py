# -*- encoding:utf-8 -*-

from ..core import db
from crm.helpers import get_user_by_token


class Team(db.Document):
    name = db.StringField(max_length=140)
    members = db.ListField(db.ReferenceField('Member'))
    leader = db.ReferenceField('Member')
    sales = db.ListField(db.ReferenceField('Sale'))
    company = db.ReferenceField('Company')

    def save(self, *args, **kwargs):
        token = kwargs['auth_token']
        user = get_user_by_token(token)
        self.company = user.company
        return super(Team, self).save(*args, **kwargs)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_leader(self):
        return self.leader
        
    def set_leader(self, leader):
        self.leader = leader

    def get_members(self):
        return self.members

    def set_members(self, members):
        self.members = members

    def set_member(self, index, member):
        self.members.insert(index, member)

    def has_member(self, member):
        return member in self.members

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member):
        self.members.remove(member)

    def get_sales(self):
        return self.sales

    def set_sales(self, sales):
        self.sales = sales

    def set_sale(self, index, sale):
        self.sales.insert(index, sale)

    def has_sale(self, sale):
        return sale in self.sales

    def add_sale(self, sale):
        self.sales.append(sale)

    def remove_sale(self, sale):
        self.sale.remove(sale)
