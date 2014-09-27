# -*- coding: utf-8 -*-
"""
    crm.api.workflow
    ----------------

    Workflow endpoints
"""

from flask import Blueprint, request, jsonify

from crm.services import process, stage, task
from crm.models import Process, Stage, Task
import json

from . import route


bp = Blueprint('workflow', __name__, url_prefix='/processes')


@route(bp, '/')
def processes():
    """
    Regresa una lista con todos los procesos de una empresa
    """
    all_process = Process.objects()
    process_dict = {}
    count = 0
    for e in all_process:
        process_dict[count] = { str(e.id) : e.get_title() }
        count = count + 1

    return {'processes': process_dict}


@route(bp, '/show/<process_id>')
def process_detail(process_id):
    """
    Regresa una instancia de proceso de una empresa
    """
    detail = Process.objects(id=process_id)

    # EN TEORIA EL SHOW DE ARRIBA Y LA FUNCION DE ABAJO DEBERIAN HACER LO MISMO
    # CUANDO SE LLAME UN PROCESO DEBE VENIR CON TODO Y TODO
    # @route(bp, '/stage/<process_id>')
    # def stage_list(process_id):
    # """
    # Regresa una lista de stages de proceso
    # """
    # process = Process.objects.get(id=process_id)
    # stages = process.get_stages()
    # all_stages = {}
    # count =  0
    # for e in stages:
    #     all_stages[count] = e.to_json()
    #     count = count + 1

    # return {'stage detail': all_stages }

    return {'process detail': detail.to_json()}


@route(bp, '/update/<process_id>', methods=['POST'])
def process_update(process_id):
    """Actualiza una instancia de proceso de una empresa"""
    title = request.form['title']
    process = Process.objects(id=process_id)
    process.update(set__title=title)
    p = Process.objects(id=process_id)

    return {'process updated': p.to_json()}


@route(bp, '/create', methods=['POST'])
def process_create():
    """Crea una instancia de proceso de una empresa"""
    p = Process()
    p.set_title(request.form['title'])
    p.save()
    id_ = str(p.id)

    return {'process': p.get_title(), 'id': id_}


@route(bp, '/destroy/<process_id>')
def process_destroy(process_id):
    """Elimina una instancia de proceso de una empresa"""
    p = Process.objects(id=process_id)
    p.delete()

    return {'processes': 'destroyed'}


#
#   CRUD STAGE
#   ----------
#

@route(bp, '/stage/show/<stage_id>')
def stage_detail(stage_id):
    """
    Regresa una instancia de stage de proceso
    de una empresa
    """
    stage = Stage.objects(id=stage_id)

    return {'stage detail': stage.to_json()}


@route(bp, '/stage/create', methods=['POST'])
def stage_create():
    """
    Crea una instancia de stage de proceso de una empresa
    """
    # SERIA MEJOR SI EL ID DEL PROCESO PADRE SE RECIBE
    # EN EL POST
    process = Process.objects.get(id=process_id)
    stage = Stage()
    stage.set_title(request.form['title'])
    stage.save()
    process.get_stages().append(stage)
    process.save()

    return {'stage': stage.to_json()}


@route(bp, '/stage/update/<stage_id>', methods=['POST'])
def stage_update(stage_id):
    """
    Actualiza una instancia de stage de proceso
    de una empresa
    """
    title = request.form['title']
    Stage.objects(id=stage_id).update_one(set__title=title)
    stage = Stage.objects(id=stage_id)

    return {'stage updated': stage.to_json()}


@route(bp, '/stage/destroy/<stage_id>')
def stage_destroy(stage_id):
    """
    Elimina una instancia de stage de proceso
    de una empresa
    """
    stage = Stage.objects(id=stage_id)
    stage.delete()
    return {'stage': 'deleted'}


#
#   CRUD TASK
#   ---------

@route(bp, '/task/show/<task_id>')
def task_detail(task_id):
    """Regresa una instancia de stage de proceso
    de una empresa"""
    # return products.get_or_404(product_id)
    task = Task.objects(id=task_id)

    return {'task detail': task.to_json()}


@route(bp, '/task/update/<task_id>', methods=['POST'])
def task_update(task_id):
    """Actualiza una instancia de stage de proceso
    de una empresa"""
    return {'task': 'update'}


@route(bp, '/task/create', methods=['POST'])
def task_create():
    """
    Crea una instancia de stage de proceso de una empresa
    """
    stage = Stage.objects.get(id=stage_id)
    task = Task()
    task.set_description(request.form['description'])
    task.save()

    stage.get_tasks().append(task)
    stage.save()

    return {'task': task.to_json()}


@route(bp, '/task/destroy/<task_id>')
def task_destroy(task_id):
    """Elimina una instancia de stage de proceso
    de una empresa"""
    # return products.get_or_404(product_id)
    task = Task.objects(id=task_id)
    task.delete()

    return {'task': 'deleted'}
