# -*- encoding:utf-8 -*-

import json

from crm.core import db
from .admin import Admin


class Company(db.Document):
    name = db.StringField(
        required=True,
        min_length=1,
        max_length=140)
    direction = db.StringField(
        required=True,
        min_length=1,
        max_length=140)
    admin = db.ReferenceField(Admin)
    items = db.ListField(db.ReferenceField('Item'))
    customers = db.ListField(db.ReferenceField('Customer'))

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_direction(self):
        return self.direction

    def set_direction(self, dir):
        self.direction = dir

    def get_admin(self):
        return self.admin

    def set_admin(self, admin):
        self.admin = admin

    @staticmethod
    def get_object(id):
        try:
            c = Company.objects.get(id=id)
            dictionary = {
                'name': c.get_name(),
                'direction': c.get_direction(),
                'admin-name': c.get_admin().get_name(),
                'admin-email': c.get_admin().get_email()
            }
            return json.dumps(dictionary)
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})

    @staticmethod
    def get_all():
        try:
            c = Company.objects()
            return c
        except db.ValidationError as e:
            return json.dumps({'errors': str(e)})

    @staticmethod
    def save_object(company, admin, password, edit=False):
        r_ad = {}
        r_co = {}

        try:
            r_ad = Admin.save_object(admin, password)
            if 'errors' not in r_ad:
                company.set_admin(admin)
            company.save(validate=True)
            r_co = company.to_json()
        except db.ValidationError as e:
            r_co = json.dumps({'errors saving admin': e.to_dict()})

        r_compa = json.loads(r_co)
        r_admin = json.loads(r_ad)

        if 'errors' in r_admin and 'errors' in r_compa:
            # All fail
            dic = Company.errors_to_dict(r_admin)
            for key in dic:
                r_compa['errors'][key] = dic[key]
            return r_compa
        elif 'errors' in r_admin and 'errors' not in r_compa:
            # Only admin fail
            dic = Company.errors_to_dict(r_admin)
            r_compa['errors'] = {}  # Clean r_compa errors
            if not edit:
            # Delete the new company saved
                company.delete()
            for key in dic:
                r_compa['errors'][key] = dic[key]
            return r_compa
        elif 'errors' not in r_admin and 'errors' in r_compa:
            # Only company fail
            if not edit:
            # Delete the new admin saved
                company.get_admin().delete()
            return r_compa
        else:
            # Nothing fail, return all the information
            if not edit:
                company.get_admin().send_mail(password)
                admin.company = company
                admin.save()
            return Company.assemble_dict(r_admin, r_compa)

    @staticmethod
    def delete_object(id):
        try:
            c = Company.objects.get(id=id)
            admin = c.get_admin()
            if admin:
                Admin.delete_object(admin.id)
            c.delete()
            return json.dumps({'success': 'The element was deleted'})
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})

    @staticmethod
    def errors_to_dict(dictio):
        dictionary = {}

        if 'name' in dictio['errors']:
            dictionary['admin-name'] = dictio['errors']['name']

        if 'email' in dictio['errors']:
            dictionary['admin-email'] = dictio['errors']['email']

        return dictionary

    @staticmethod
    def assemble_dict(d_admin, d_compa):

        d_compa['admin-name'] = d_admin['name']
        d_compa['admin-email'] = d_admin['email']

        return d_compa