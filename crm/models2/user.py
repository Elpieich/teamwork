# -*- encoding:utf-8 -*-

from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from crm.core import db, mail
from .role import Role
import json

login_serializer = URLSafeTimedSerializer('FLAKSDJFdLKJ98798}{}{}KAJSDHFK22a')


class User(db.Document):
    name = db.StringField(
        required=True,
        min_length=1,
        max_length=140)
    password = db.StringField(
        required=True,
        min_length=8,
        max_length=50)
    token = db.StringField()
    email = db.EmailField(
        required=True,
        unique=True)
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

    def get_token(self):
        return self.token

    def generate_auth_token(self):
        """
        Encode a secure token for cookie
        """
        data = [str(self.id), self.password]
        self.token = login_serializer.dumps(data)

    def send_mail(self):
        txt = 'Hello, now you have access to CRM API \n ' \
            'Your user is: %s \n Your password is: %s \n' \
            'Your token (for API purposes) is: %s \n\n' \
            '------------------------- \n\n Enjoy' % (
            self.get_email(),
            self.get_password(),
            self.get_token())

        msg = Message(
            'Welcome to CRM API',
            sender="crmsuscriptions@gmail.com",
            recipients=
            [self.get_email()])
        msg.body = txt
        mail.send(msg)

    @staticmethod
    def get_object(id):
        try:
            u = User.objects.get(id=id)
            return u.to_json()
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})

    @staticmethod
    def get_all(user_type):
        try:
            users = User.objects(
                role=Role.objects.get(name=user_type))
            return users
        except db.ValidationError as e:
            return json.dumps({'errors': str(e)})

    @staticmethod
    def save_object(user, mail=False):
        try:
            user.save(validate=True)
            if mail:
                user.send_mail()
            return user.to_json()
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})
        except db.NotUniqueError:
            return json.dumps({'errors': {'email': 'This email is already registered'}})

    @staticmethod
    def delete_object(id):
        try:
            User.objects.get(id=id).delete()
            return json.dumps({'success': 'The element was deleted'})
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})