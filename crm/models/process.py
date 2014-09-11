# -*- encoding:utf-8 -*-

from crm.core import db
from .stage import StageTemplate, Stage
from .company import Company


class ProcessTemplate(db.Document):
    __name__ = db.StringField(
        max_length=40,
        required=True)
    __description__ = db.StringField(
        max_length=140,
        required=True)
    __company__ = db.ReferenceField(Company)
    __stages__ = db.ListField(
        db.ReferenceField(StageTemplate))

    meta = {
        'allow_inheritance': True
    }

    def get_name(self):
        return self.__name__

    def get_description(self):
        return self.__description__

    def get_company(self):
        return self.__company__

    def get_stages(self):
        return self.__stages__


class Process(db.Document, ProcessTemplate):
    __template__ = db.ReferenceField(ProcessTemplate)
    __title__ = db.StringField()
    __stages__ = db.ListField(
        db.ReferenceField(Stage))

    def get_title(self):
        return self.__title__

    def set_title(self, title):
        self.__title__ = title

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

    def __str__(self):
        return self.__title__