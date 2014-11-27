# -*- encoding:utf-8 -*-

from crm.core import db
import json


class Permission(db.Document):
    name = db.StringField(
        required=True,
        min_length=1,
        max_length=140)
    description = db.StringField(
        required=True,
        min_length=1,
        max_length=140)

    @db.queryset_manager
    def objects(doc_cls, queryset):
        return queryset.order_by('+name')

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, desc):
        self.description = desc

    @staticmethod
    def get_object(id):
        try:
            p = Permission.objects.get(id=id)
            return p.to_json()
        except db.ValidationError as e:
            return json.dumps({'errors': str(e)})

    @staticmethod
    def get_all():
        try:
            p = Permission.objects()
            return p
        except db.ValidationError as e:
            return json.dumps({'errors': str(e)})

    @staticmethod
    def save_object(permission):
        try:
            permission.save(validate=True)
            return permission.to_json()
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})

    @staticmethod
    def delete_object(id):
        try:
            Permission.objects.get(id=id).delete()
            return json.dumps({'success': 'The element was deleted'})
        except db.ValidationError as e:
            return json.dumps({'errors': e.to_dict()})