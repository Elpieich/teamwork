# -*- coding: utf-8 -*-
"""
    crm.api.template
    ----------------

    Template endpoints
"""

from flask import Blueprint, request

from crm.services import process_template
from . import route


bp = Blueprint('template', __name__, url_prefix='/templates')


@route(bp, '/')
def process_templates():
    """Regresa una lista con todos los templates de procesos
    de una empresa
    """
    return process_template.all()


@route(bp, '/', methods=['POST'])
def process_template_create():
    """Crea una instancia de template de proceso de una empresa
    """
    return process_template.create()


@route(bp, '/<template_id>')
def process_template_detail(template_id):
    """Regresa una instancia de template de proceso
    de una empresa
    """
    return process_template.detail()


@route(bp, '/<template_id>', methods=['UPDATE'])
def process_template_update(template_id):
    """Actualiza una instancia de template de proceso
    de una empresa
    """
    return process_template.update()


@route(bp, '/<template_id>', methods=['DELETE'])
def process_template_delete(template_id):
    """Elimina una instancia de template de proceso
    de una empresa
    """
    return process_template.delete()
