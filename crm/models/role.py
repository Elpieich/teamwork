# -*- encoding:utf-8 -*-

from crm.core import db
from .permission import Permission


class Role(db.Document):
    name = db.StringField(required=True)
    description = db.StringField(required=True)
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
                p_aux = Permission.objects.get(id=k)#.first()
                self.permissions.append(p_aux)
        # Refresh role
        self.save()


    def has_permission(self):
        pass
