# -*- coding: utf-8 -*-
"""

"""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from crm.apps.website import Website
from crm.apps.api import API
from crm.apps.admin import Admin

api = API()
website = Website()
admin = Admin()

application = DispatcherMiddleware(
	website.get_app(),
    {'/api/1': api.app,
	 '/admin': admin.app})

if __name__ == "__main__":
    run_simple(
        '0.0.0.0',
        5000,
        application,
        use_reloader=True,
        use_debugger=True)
