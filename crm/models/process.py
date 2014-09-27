# -*- encoding:utf-8 -*-

from ..core import db


class ProcessType(db.Document):
    description = db.StringField(
        max_length=140,
        required=True)
    

class ProcessStatus(db.Document):
    description = db.StringField(
        max_length=40,
        required=True)


class ProcessTemplate(db.Document):
    name = db.StringField(
        max_length=40,
        required=True)
    description = db.StringField(
        max_length=140,
        required=True)
    type = db.ReferenceField('ProcessType')
    company = db.ReferenceField('Company')
    stage_templates = db.ListField(
        db.ReferenceField('StageTemplate'))

    meta = {
        'allow_inheritance': True
    }


class Process(db.Document):
    name = db.StringField(
        max_length=40,
        required=True)
    description = db.StringField(
        max_length=140,
        required=True)
    template = db.ReferenceField('ProcessTemplate')
    team = db.ReferenceField('Team')
    manager = db.ReferenceField('User')
    status = db.ReferenceField('ProcessStatus')
    stages = db.ListField(
        db.ReferenceField('Stage'))
    parent = db.ReferenceField('Process')
    variables = db.ListField()
