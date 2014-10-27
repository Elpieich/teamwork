# -*- encoding:utf-8 -*-

from ..core import db


#DynamicDocument -> agregar campos en ejecución y los guarda
#EmbeddedDocument -> documentos que no son necesarios en coleccion, solo se usan como referencia
#db.ReferenceField('ProcessTemplate',reverse_delete_rule=db.CASCADE) -> si borran ProcessTemplate se van los stages que tengan esto
#As BSON (the binary format for storing data in mongodb) is order dependent, documents are serialized based on their field order.There is one caveat on Dynamic Documents: fields cannot start with _
#Dynamic fields are stored in creation order after any declared fields.
#foro 21 oct  3pm a 7pm sum prepa 2


TYPES = (
    ('SALES', 'SALES', ))


class ProcessTemplate(db.Document):
    name = db.StringField(max_length=40, required=True)
    description = db.StringField(max_length=140, required=True)
    type = db.StringField(choices=TYPES)
    company = db.ReferenceField('Company', reverse_delete_rule=db.CASCADE)
    stage_templates = db.ListField(db.EmbeddedDocumentField('StageTemplate'))

    meta = {
        'allow_inheritance': True
    }

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

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_company(self):
        return self.company

    def set_company(self, company):
        self.company = company

    def get_stage_templates(self):
        return self.stage_templates

    def set_stage_templates(self, stage_template):
        self.stage_templates.append(stage_template)

    def get_stage_template(self, stage_id):
        for stage in self.stage_templates:
            if stage.get_id() == stage_id:
                return stage
        return None
