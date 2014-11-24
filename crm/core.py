# -*- encoding:utf-8 -*-

from flask_login import LoginManager
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension
from flask_security import Security
from flask_security import MongoEngineUserDatastore

mail = Mail()
db = MongoEngine()
login_manager = LoginManager()
user_datastore = MongoEngineUserDatastore
security = Security()
toolbar = DebugToolbarExtension()
