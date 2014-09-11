# -*- encoding:utf-8 -*-

from crm.core import db
from task import TaskTemplate, Task
from process import ProcessTemplate


class StageTemplate(db.Document):
    __name = db.StringField(max_length=40, required=True)
    __process = db.ReferenceField(ProcessTemplate)
    __tasks = db.ListField(db.ReferenceField(TaskTemplate))

    meta = {'allow_inheritance': True }

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_process(self):
        return self.__process

    def get_tasks(self):
        return self.__tasks


class Stage(db.Document, StageTemplate):
    __template = db.ReferenceField(StageTemplate)
    __tasks = db.ListField(db.ReferenceField(Task))

    # Setters and Getters
    def get_name():
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_tasks(self):
        return self.__tasks

    def set_tasks(self, tasks):
        self.__tasks = tasks

    # More Functions

    def add_task(self):
        pass

    def remove_task(self):
        pass

    def is_finalized(self):
        pass
