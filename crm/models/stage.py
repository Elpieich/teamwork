# -*- encoding:utf-8 -*-

from crm.core import db
from task import TaskTemplate, Task
from process import ProcessTemplate


class StageTemplate(db.Document):
    __name__ = db.StringField(
        max_length=40,
        required=True)
    __process__ = db.ReferenceField(ProcessTemplate)
    __tasks__ = db.ListField(
        db.ReferenceField(TaskTemplate))

    meta = {
        'allow_inheritance': True
    }

    def get_name(self):
        return self.__name__

    def get_process(self):
        return self.__process__

    def get_tasks(self):
        return self.__tasks__


class Stage(db.Document, StageTemplate):
    __template__ = db.ReferenceField(StageTemplate)
    __tasks__ = db.ListField(
        db.ReferenceField(Task))

    def add_task(self):
        pass

    def remove_task(self):
        pass

    def is_finalized(self):
        pass

    def get_tasks(self):
        return self.__tasks__

    def set_tasks(self, tasks):
        self.__tasks__ = tasks

