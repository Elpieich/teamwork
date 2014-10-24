# -*- encoding:utf-8 -*-

from crm.core import db
from .role import Role
import json


class User(db.Document):
    name = db.StringField(
        required=True,
        min_length=1,
        max_length=140)
    password = db.StringField(
        required=True,
        min_length=8,
        max_length=50)
    email = db.EmailField(required=True)
    role = db.ReferenceField(Role)

    meta = {'allow_inheritance': True}

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

    def set_password(self, passw):
        self.password = passw

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def get_object(id):
        try:
            u = User.objects.get(id=id)
            return u.to_json()
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})

    @staticmethod
    def get_all(user_type):
        return User.objects(
            role=Role.objects.get(name=user_type)
        )

    @staticmethod
    def save_object(user):
        try:
            user.save(validate=True)
            return user.to_json()
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})

    @staticmethod
    def delete_object(id):
        try:
            User.objects.get(id=id).delete()
            return json.dumps({'success': 'The element was deleted'})
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})