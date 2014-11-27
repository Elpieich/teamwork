# -*- encoding:utf-8 -*-

from ..core import db
from . import User


class Member(User, db.EmbeddedDocument):
    pass