# -*- coding: utf-8 -*-
"""
    crm.admin.views.log
    ----------------

    crm panel admin log views
"""

from flask import request, render_template, g, redirect, Blueprint

from crm.models_admin.log import Log
from ..helpers import login_required


bp = Blueprint('log', __name__, template_folder='templates')

@bp.route('/logs', methods=['GET'])
@login_required
def logs():
    """Get all the logs
    """
    result = Log.get_all()
    setattr(g, 'result', result)
    return render_template('logs.html', logs=result)