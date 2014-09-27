# -*- encoding:utf-8 -*-

from crm.core import db


class TaskTemplate(db.Document):
    description = db.StringField(
        max_length=140,
        required=True)
    stage_template = db.ReferenceField('StageTemplate')

    meta = {
        'allow_inheritance': True
    }


class Task(TaskTemplate):
    description = db.StringField(
        max_length=140,
        required=True)
    template = db.ReferenceField('TaskTemplate')
    stage = db.ReferenceField('Stage')
    completed = db.BooleanField(
        default=False)
    completed_by = db.ReferenceField('User')
    manager = db.ReferenceField('User')
    progress = db.IntField()
