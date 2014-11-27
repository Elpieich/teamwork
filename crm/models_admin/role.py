# -*- encoding:utf-8 -*-

from crm.core import db
from .permission import Permission
import json


class Role(db.Document):
    name = db.StringField(
        required=True,
        min_length=1,
        max_length=140)
    description = db.StringField(
        required=True,
        min_length=1,
        max_length=140)
    permissions = db.ListField(db.ReferenceField(Permission))

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, desc):
        self.description = desc

    def get_permissions(self):
        return self.permissions

    def add_permissions(self, perms):
        """
            Get all the permissions
        
            perms: json object
        """
        
        # Clean list
        self.permissions[:] = []

        for k in perms:
            if perms[k]:
                p_aux = Permission.objects.get(id=k)
                self.permissions.append(p_aux)
        # Refresh role
        self.save()

    def has_permission(self, perm):
        return perm in self.permissions


    @staticmethod
    def get_object(id):
        try:
            r = Role.objects.get(id=id)
            return r.to_json()
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})

    @staticmethod
    def get_all():
        try:
            roles = Role.objects()
            return roles
        except db.ValidationError as e:
            return json.dumps({'errors': str(e)})

    @staticmethod
    def save_object(role, permissions):
        try:
            role.save(validate=True)
            role.add_permissions(permissions)
            return role.to_json()
        except db.ValidationError as e:
            print e.to_dict()
            return json.dumps({'errors': e.to_dict()})

    @staticmethod
    def delete_object(id):
        try:
            Role.objects.get(id=id).delete()
            return json.dumps({'success': 'The element was deleted'})
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})