# -*- coding: utf-8 -*-
"""
    crm.api.template
    ----------------

    Auth endpoints
"""

from flask import Blueprint, current_app

from crm.services import user
from crm.core import db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/', methods=['POST'], strict_slashes=False)
def auth():
    """
    """
    service = user(authenticate=True)
    try:    
        response = service.authenticate()
    except db.DoesNotExist as exception:
    	response = str(exception)
    except db.ValidationError as exception:
        response = str(exception)
    return current_app.output_format(response)
