# -*- coding: utf-8 -*-
"""
    crm.api.template
    ----------------

    Auth endpoints
"""

from flask import Blueprint, current_app

from crm.services import user


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/', methods=['POST'], strict_slashes=False)
def auth():
    """
    """
    service = user(authenticate=True)
    return current_app.output_format(service.authenticate())
