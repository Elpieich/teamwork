# -*- encoding:utf-8 -*-

from ..core import db
from . import User


class Member(User, db.EmbeddedDocument):

    def get_auth_token(self):
        return super(Member, self).get_auth_token()