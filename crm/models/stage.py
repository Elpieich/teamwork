# -*- encoding:utf-8 -*-

from ..core import db


class StageStatus(db.Document):
    description = db.StringField(
        max_length=40,
        required=True)


class StageTemplate(db.Document):
    name = db.StringField(
        max_length=40,
        required=True)
    description = db.StringField(
        max_length=40)
    process_template = db.ReferenceField('ProcessTemplate')
    task_templates = db.ListField(
        db.ReferenceField('TaskTemplate'))

    meta = {
        'allow_inheritance': True
    }


class Stage(db.Document):
    name = db.StringField(
        max_length=40,
        required=True)
    description = db.StringField(
        max_length=40)
    template = db.ReferenceField('StageTemplate')
    process = db.ReferenceField('Process')
    sub = db.ReferenceField('Process')
    template = db.ReferenceField('StageTemplate')
    manager = db.ReferenceField('User')
    status = db.ReferenceField('StageStatus')
    logic = db.ListField()
    variables = db.ListField()
    initial_date = db.DateTimeField()
    final_date = db.DateTimeField()
    tasks = db.ListField(
        db.ReferenceField('Task'))
