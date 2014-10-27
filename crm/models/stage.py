# -*- encoding:utf-8 -*-

from ..core import db


class Stage(db.Document):
    name = db.StringField(max_length=40, required=True)
    description = db.StringField(max_length=140)
    template = db.ReferenceField('StageTemplate')
    process = db.ReferenceField('Process')
    template = db.ReferenceField('StageTemplate')
    manager = db.ReferenceField('User')
    status = db.ReferenceField('StageStatus')
    tasks = db.ListField(db.ReferenceField('Task'))
