# -*- coding: utf-8 -*-
"""
    crm.api.workflow
    ----------------

    Workflow endpoints
"""

from flask import Blueprint, request, jsonify


from crm.services import process, stage, task
from crm.models.all import *
import json

from . import route


bp = Blueprint('workflow', __name__, url_prefix='/processes')


#
#   CRUD PROCESOS
#   -------------
#
@route(bp, '/')
def processes():
    """Regresa una lista con todos los procesos de una empresa"""
    #return products.all()
    p = Process.objects()

    return {'processes': p.to_json()}


@route(bp, '/show/<process_id>')
def process_detail(process_id):
    """Regresa una instancia de proceso de una empresa"""
    detail = Process.objects(id=process_id)

    return {'process detail': detail.to_json()}


@route(bp, '/update/<process_id>', methods=['POST'])
def process_update(process_id):
    """Actualiza una instancia de proceso de una empresa"""
    title = request.form['title']
    Process.objects(id=process_id).update_one(set__title=title)
    p = Process.objects(id=process_id)

    return {'process updated': p.to_json()}


@route(bp, '/create', methods=['POST'])
def process_create():
    """Crea una instancia de proceso de una empresa"""
    p = Process()
    p.set_title(request.form['title'])
    p.save()
    id = str(p.id)

    return {'process': p.get_title(),
            'id': id}


@route(bp, '/destroy/<process_id>')
def process_destroy(process_id):
    """Elimina una instancia de proceso de una empresa"""
    # return products.get_or_404(product_id)
    # Process.objects.remove({'_id' : ObjectId(process_id)})
    return {'processes': 'destroy'}


#
#   CRUD STAGE
#   ----------
#
@route(bp, '/stage/show/<stage_id>')
def stage_detail(stage_id):
    """Regresa una instancia de stage de proceso
    de una empresa"""
    stage = Stage.objects(id=stage_id)

    return {'stage detail': stage.to_json()}


@route(bp, '/stage/update/<stage_id>', methods=['POST'])
def stage_update(stage_id):
    """Actualiza una instancia de stage de proceso
    de una empresa"""
    title = request.form['title']
    Stage.objects(id=stage_id).update_one(set__title=title)
    p = Stage.objects(id=stage_id)

    return {'stage updated': p.to_json()}


@route(bp, '/stage/create', methods=['POST'])
def stage_create():
    """Crea una instancia de stage de proceso de una empresa """
    s = Stage()
    s.set_title(request.form['title'])
    s.save()
    id = str(s.id)

    return {'stage': s.get_title(),
            'id': id}


@route(bp, '/stage/destroy/<stage_id>')
def stage_destroy(stage_id):
    """Elimina una instancia de stage de proceso
    de una empresa"""
    # return products.get_or_404(product_id)
    return {'stage': 'destroy'}


#
#   CRUD TASK
#   ---------
#
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
    """Crea una instancia de stage de proceso de una empresa """
    t = Task()
    t.set_description(request.form['description'])
    t.save()
    return {'task': t.get_description(),
            'id': t.id}


@route(bp, '/task/destroy/<task_id>')
def task_destroy(task_id):
    """Elimina una instancia de stage de proceso
    de una empresa"""
    # return products.get_or_404(product_id)
    return {'task': 'destroy'}
