# -*- encoding:utf-8 -*-

from ..core import db



class User(db.Document):
    name = db.StringField(required=True, min_length=4, max_length=140)
    password = db.StringField(required=True, min_length=8, max_length=50)
    token = db.StringField()
    email = db.EmailField(required=True, unique=True)
    role = db.ReferenceField('Role')

    meta = {'allow_inheritance': True}

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_role(self):
        return self.role

    def set_role(self, role):
        self.role = role

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_token(self):
        return self.token
