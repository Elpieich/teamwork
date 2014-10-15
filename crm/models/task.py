# -*- encoding:utf-8 -*-

from ..core import db
from ..helpers import JsonSerializer



class Task(JsonSerializer, db.Document):
    description = db.StringField(
        max_length=140,
        required=True)
    template = db.ReferenceField('TaskTemplate')
    stage = db.ReferenceField('Stage')
    completed = db.BooleanField(
        default=False)
    #completed_by = db.ReferenceField('User')
    #manager = db.ReferenceField('User')
    progress = db.IntField()
