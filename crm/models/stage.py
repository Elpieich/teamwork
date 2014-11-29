# -*- encoding:utf-8 -*-

from ..core import db
from crm.helpers import get_user_by_token

STATUS = (
    ('A', 'Abierta', ),
    ('B', 'En espera', ),
    ('C', 'Cancelada', ),
    ('D', 'Cerrada'), )


class Stage(db.Document):
    name = db.StringField(max_length=40, required=True)
    description = db.StringField(max_length=140)
    process = db.ReferenceField('Process')
    template = db.ReferenceField('StageTemplate')
    manager = db.ReferenceField('User')
    status = db.StringField(choices=STATUS)
    tasks = db.ListField(db.ReferenceField('Task'))
    company = db.ReferenceField('Company')

    def save(self, *args, **kwargs):
        token = kwargs['auth_token']
        user = get_user_by_token(token)
        self.company = user.company
        return super(Stage, self).save(*args, **kwargs)