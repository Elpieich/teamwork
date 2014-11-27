# -*- encoding:utf-8 -*-

from ..core import db
from crm.helpers import get_user_by_token


STATUS = (
    ('A', 'Abierta', ),
    ('B', 'En espera', ),
    ('C', 'Cancelada', ),
    ('D', 'Cerrada'), )


class Process(db.Document):
    name = db.StringField(max_length=40, required=True)
    description = db.StringField(max_length=140, required=True)
    template = db.ReferenceField('ProcessTemplate')
    status = db.StringField(choices=STATUS)
    stages = db.ListField(db.ReferenceField('Stage'))
    company = db.ReferenceField('Company')

    def save(self, *args, **kwargs):
        token = kwargs['auth_token']
        user = get_user_by_token(token)
        self.company = user.company
        return super(Process, self).save(*args, **kwargs)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_stages(self):
        return self.stages

    def set_stages(self, stages):
        self.stages = stages

    def add_stage(self, stage):
        self.stages.append(stage)

    def remove_stage(self, stage):
        self.stages.remove(stage)
