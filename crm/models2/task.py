# -*- encoding:utf-8 -*-

from ..core import db


class Task(db.Document):
    description = db.StringField(max_length=140, required=True)
    stage = db.ReferenceField('Stage')
    completed = db.BooleanField(default=False)
    owner = db.ReferenceField('User')
    manager = db.ReferenceField('User')
    progress = db.IntField(max_value=100, min_value=0)

    def get_id(self):
        return self.id
        
    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_stage(self):
        return self.stage

    def set_stage(self, stage):
        self.stage = stage

    def get_completed(self):
        return self.completed

    def set_completed(self, completed):
        self.completed = completed

    def get_owner(self):
        return self.owner

    def set_owner(self, owner):
        self.owner = owner

    def get_manager(self):
        return self.manager

    def set_manager(self, manager):
        self.manager = manager

    def get_progress(self):
        return self.progress

    def set_progress(self, progress):
        self.progress = progress
