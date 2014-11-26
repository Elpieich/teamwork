# -*- encoding:utf-8 -*-

from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension
from flask_security import Security


mail = Mail()
db = MongoEngine()
security = Security()
toolbar = DebugToolbarExtension()
