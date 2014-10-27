# -*- encoding:utf-8 -*-


# from flask_sqlalchemy import SQLAlchemy
# from flask_security import Security, SQLAlchemyUserDatastore

from flask_login import LoginManager
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension
from flask_security import Security, MongoEngineUserDatastore


mail = Mail()
db = MongoEngine()
login_manager = LoginManager()
security = Security()
toolbar = DebugToolbarExtension()
