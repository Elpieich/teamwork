# -*- encoding:utf-8 -*-

#from flask_mail import Mail
# from flask_sqlalchemy import SQLAlchemy
# from flask_security import Security, SQLAlchemyUserDatastore


from flask_mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

#db = SQLAlchemy()
#mail = Mail()
#security = Security()
#social = Social()
db = MongoEngine()
toolbar = DebugToolbarExtension()
login_manager = LoginManager()
