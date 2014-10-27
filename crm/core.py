# -*- encoding:utf-8 -*-

from flask_mail import Mail
# from flask_sqlalchemy import SQLAlchemy
# from flask_security import Security, SQLAlchemyUserDatastore


from flask_mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension
from flask_security import Security, MongoEngineUserDatastore

#    UserMixin, RoleMixin, login_required

#db = SQLAlchemy()
mail = Mail()
#security = Security()
#social = Social()
db = MongoEngine()
#user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security()#app, user_datastore)
toolbar = DebugToolbarExtension()