# -*- encoding:utf-8 -*-

from ..core import db


class StageTemplate(db.EmbeddedDocument):
    name = db.StringField(max_length=40, required=True)
    description = db.StringField(max_length=40)
    process_template = db.ReferenceField('ProcessTemplate')
    order = db.IntField()
    next = db.ReferenceField('StageTemplate', default=None)
    prev = db.ReferenceField('StageTemplate', default=None)
    #task_templates = db.ListField(db.ReferenceField('TaskTemplate'))

    meta = {'allow_inheritance': True }

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

    def get_next(self):
        return self.next

    def set_next(self, stage_template):
        self.next = stage_template

    def get_prev(self):
        return self.prev

    def set_prev(self, stage_template):
        self.prev = stage_template
