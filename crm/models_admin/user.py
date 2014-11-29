# -*- encoding:utf-8 -*-

import json
from itsdangerous import URLSafeTimedSerializer

from flask_mail import Message
from flask_security.core import UserMixin, current_user
from flask_security.utils import get_hmac, verify_password

from .role import Role
from crm.core import db, mail


login_serializer = URLSafeTimedSerializer('FLAKSDJFdLKJ98798}{}{}KAJSDHFK22a')


class User(db.Document, UserMixin):
    name = db.StringField(required=True, min_length=1, max_length=140)
    password = db.StringField(required=True, min_length=8)
    token = db.StringField()
    email = db.EmailField(required=True, unique=True)
    roles = db.ListField(db.ReferenceField('Role'), default=[])
    company = db.ReferenceField('Company')
    active = db.BooleanField(default=True)
    meta = {'allow_inheritance': True}

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_company(self):
        self.company

    def set_company(self, company):
        self.company = company

    def add_role(self, role):
        self.roles.append(role)

    def get_token(self):
        return self.token

    def generate_auth_token(self):
        """
        Encode a secure token for cookie
        """
        data = [str(self.id), self.password]
        self.token = login_serializer.dumps(data)

    def is_correct_password(self, password):
        """
        Verify if the password is correct
        """
        return verify_password(password, self.password)

    def send_mail(self, password):
        """
        Send a email to the user created
        """
        txt = 'Hello, now you have access to CRM API \n ' \
            'Your user is: %s \n Your password is: %s \n' \
            '------------------------- \n\n Enjoy' % (
            self.get_email(),
            password)

        msg = Message(
            'Welcome to CRM API',
            sender="crmsuscriptions@gmail.com",
            recipients=
            [self.get_email()])
        msg.body = txt
        mail.send(msg)

    @staticmethod
    def encrypt(string):
        return get_hmac(string)


    @staticmethod
    def generate_password():
        user = User()
        user.generate_auth_token()
        string = user.get_token()
        password = login_serializer.dumps([string[:5], string[5:10]])
        return password[:9]

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
                roles=Role.objects.get(name=user_type))
            return users
        except db.ValidationError as e:
            return json.dumps({'errors': str(e)})

    @staticmethod
    def save_object(user, password, mail=False):
        try:
            user.save(validate=True)
            if mail:
                user.send_mail(password)
            return user.to_json()
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})
        except db.NotUniqueError:
            return json.dumps({'errors': {'email': 'This email is already registered'}})

    @staticmethod
    def delete_object(id):
        try:
            if str(current_user.id) == id:
                return json.dumps({'errors': 'You cant delete your own user'})
            else:
                User.objects.get(id=id).delete()
                return json.dumps({'success': 'The element was deleted'})
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})

    @staticmethod
    def get_admin(email):
        try:
            user = User.objects.get(email=email)
            if user.has_role('Administrator API panel'):
                return user
            else:
                return 'errors: user is not administrator'
        except db.DoesNotExist:
            return 'errors'