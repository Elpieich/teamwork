# -*- encoding:utf-8 -*-

# from flask_sqlalchemy import SQLAlchemy
# from flask_security import Security, SQLAlchemyUserDatastore

from flask_mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail

#db = SQLAlchemy()
#security = Security()
#social = Social()
db = MongoEngine()
toolbar = DebugToolbarExtension()
login_manager = LoginManager()
mail = Mail()