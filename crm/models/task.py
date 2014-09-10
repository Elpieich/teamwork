# -*- encoding:utf-8 -*-

from crm.core import db
from .stage import StageTemplate


class TaskTemplate(db.Document):
    __description__ = db.StringField(
        max_length=140,
        required=True)
    __stage__ = db.ReferenceField(StageTemplate)

    meta = {
        'allow_inheritance': True
    }

    def get_name(self):
        return self.__name__

    def get_stage(self):
        return self.__stage__


class Task(db.Document, TaskTemplate):
    __template__ = db.ReferenceField(TaskTemplate)
    __description__ = db.StringField()
    __completed__ = db.BooleanField()

    def get_description(self):
        return self.__description__

    def set_description(self, desc):
        self.__description__ = desc

    def complete_task(self):
        self.__completed__ = True

    def uncomplete_task(self):
        self.__completed__ = False
