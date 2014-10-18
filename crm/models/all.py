# -*- encoding:utf-8 -*-

from crm.core import db
from mongoengine import  *
from crm.models import *

class Task(db.Document):
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


class Stage(db.Document):
    title = db.StringField()
    __tasks__ = db.ListField(
        db.ReferenceField(Task))

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

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


class Process(db.Document):
    title = db.StringField()
    __stages__ = db.ListField(
        db.ReferenceField(Stage))

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_stages(self):
        return self.__stages__

    def set_stages(self, stages):
        self.__stages__ = stages

    def add_stage(self, stage):
        pass

    def remove_stage(self, position):
        pass

    def get_latest_stage(self):
        pass
