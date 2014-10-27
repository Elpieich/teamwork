# -*- encoding:utf-8 -*-

from ..core import db
from ..helpers import JsonSerializer

#next
#prev
#orden 

class StageTemplate(db.EmbeddedDocument):
    name = db.StringField(
        max_length=40,
        required=True)
    description = db.StringField(
        max_length=40)
    process_template = db.ReferenceField('ProcessTemplate')#,
                                         #reverse_delete_rule=db.CASCADE)
    task_templates = db.ListField(
        db.ReferenceField('TaskTemplate'))

    meta = {'allow_inheritance': True }


