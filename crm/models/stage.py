# -*- encoding:utf-8 -*-

from ..core import db
from ..helpers import JsonSerializer


class Step(JsonSerializer, db.Document):
    name = db.StringField(
        max_length=40,
        required=True)
    description = db.StringField(
        max_length=40)
    template = db.ReferenceField('StageTemplate')
    process = db.ReferenceField('Process')
    sub = db.ReferenceField('Process')
    template = db.ReferenceField('StageTemplate')
    #manager = db.ReferenceField('User')
    status = db.ReferenceField('StageStatus')
    logic = db.ListField()
    variables = db.ListField()
    initial_date = db.DateTimeField()
    final_date = db.DateTimeField()
    tasks = db.ListField(
        db.ReferenceField('Task'))
