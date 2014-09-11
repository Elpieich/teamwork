# -*- encoding:utf-8 -*-

from crm.core import db
from .stage import StageTemplate, Stage
from .company import Company


class ProcessTemplate(db.Document):
    __name = db.StringField(max_length=40, required=True)
    __description = db.StringField(max_length=140, required=True)
    __company = db.ReferenceField(Company)
    __stages = db.ListField(db.ReferenceField(StageTemplate))

    meta = {'allow_inheritance': True }

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_company(self):
        return self.__company

    def get_stages(self):
        return self.__stages


class Process(db.Document, ProcessTemplate):
    __template = db.ReferenceField(ProcessTemplate)
    __title = db.StringField()
    __stages = db.ListField(db.ReferenceField(Stage))

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def get_stages(self):
        return self.__stages

    def set_stages(self, stages):
        self.__stages = stages

    def add_stage(self, stage):
        self__stages

    def remove_stage(self, position):
        pass

    def get_latest_stage(self):
        pass

    def __str__(self):
        return self.__title
