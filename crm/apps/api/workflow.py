# -*- coding: utf-8 -*-
"""
    crm.api.workflow
    ----------------

    Workflow endpoints
"""

from flask import Blueprint, request

from crm.services import process, stage, task
from crm.service import route


bp = Blueprint('workflow', __name__)


#
#    PROCESSES
#   -----------
#
@route(bp, '/processes')
def processes():
    """
    Regresa una lista con todos los procesos de una empresa
    """
    service = process()
    return service.all()

@route(bp, '/processes', methods=['POST'])
def process_create():
    """Crea una instancia de proceso de una empresa
    """
    service = process()
    return service.create()

@route(bp, '/processes/<process_id>')
def process_detail(process_id):
    """
    Regresa una instancia de proceso de una empresa
    """
    service = process()
    return service.get(process_id)

@route(bp, '/processes/<process_id>', methods=['UPDATE'])
def process_update(process_id):
    """Actualiza una instancia de proceso de una empresa
    """
    service = process()
    return service.update(process_id)

@route(bp, '/processes/<process_id>', methods=['DELETE'])
def process_delete(process_id):
    """Elimina una instancia de proceso de una empresa
    """
    service = process()
    return service.delete(process_id)

@route(bp, '/processes/<process_id>/stages')
def process_stages(process_id):
    """
    Regresa una lista de stages de proceso
    """
    service = process()
    return service.get(process_id, full=True)

@route(bp, '/processes/search')
def processes_search():
    """
    Regresa una lista con todos los procesos 
    de una empresa que coinciden con los filtros
    de busqueda
    """
    service = process()
    return service.find()


#
#    STAGES
#   --------
#
@route(bp, '/stages', methods=['POST'])
def stage_create():
    """
    Crea una instancia de stage de proceso 
    de una empresa
    """
    service = stage()
    return service.create()

@route(bp, '/stages/<stage_id>')
def stage_detail(stage_id):
    """
    Regresa una instancia de stage de proceso
    de una empresa
    """
    service = stage()
    return service.get(stage_id)

@route(bp, '/stages/<stage_id>', methods=['UPDATE'])
def stage_update(stage_id):
    """
    Actualiza una instancia de stage de proceso
    de una empresa
    """
    service = stage()
    return service.update(stage_id)

@route(bp, '/stages/<stage_id>', methods=['DELETE'])
def stage_delete(stage_id):
    """
    Elimina una instancia de stage de proceso
    de una empresa
    """
    service = stage()
    return service.delete(stage_id)

@route(bp, '/stages/<stage_id>/tasks')
def stage_tasks(stage_id):
    """
    Regresa una instancia de stage con la lista de
    task completa
    """
    service = stage()
    return service.get(stage_id, full=True)

@route(bp, '/stages/search')
def stages_search():
    """
    Regresa una lista con todos los stages de una empresa que coinciden 
    con los filtros de busqueda
    """
    service = stage()
    return service.find()


#
#    TASKS
#   -------
#
@route(bp, '/tasks', methods=['POST'])
def task_create():
    """
    Crea una instancia de stage de proceso de una empresa
    """
    service = task()
    return service.create()

@route(bp, '/tasks/<task_id>')
def task_detail(task_id):
    """Regresa una instancia de stage de proceso
    de una empresa
    """
    service = task()
    return service.get(task_id)

@route(bp, '/tasks/<task_id>', methods=['UPDATE'])
def task_update(task_id):
    """Actualiza una instancia de stage de proceso
    de una empresa
    """
    service = task()
    return service.update(task_id)

@route(bp, '/tasks/<task_id>', method=["DELETE"])
def task_delete(task_id):
    """Elimina una instancia de stage de proceso
    de una empresa
    """
    service = task()
    return service.delete(task_id)

@route(bp, '/tasks/search')
def tasks_search():
    """
    Regresa una lista con todos los tasks
    de una empresa que coinciden con los filtros
    de busqueda
    """
    service = task()
    return service.find()
