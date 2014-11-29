# -*- coding: utf-8 -*-

import json
import datetime

from crm.core import db
from crm.models_admin.user import User


class Log(db.Document):
    ip = db.StringField()
    url = db.StringField()
    method = db.StringField()
    user = db.ReferenceField(User)
    result = db.StringField()
    creation_date = db.DateTimeField(default=datetime.datetime.now)

    @db.queryset_manager
    def objects(doc_cls, queryset):
        # Get the objects by descending date
        return queryset.order_by('-creation_date')

    @staticmethod
    def get_all():
        try:
            logs = Log.objects()
            return logs
        except db.ValidationError as e:
            return json.dumps({'errors': str(e)})

    @staticmethod
    def save_object(ip, url, method, user, result):
        try:
            log = Log()
            log.ip = ip
            log.url = url
            log.method = method
            log.user = user

            if isinstance(result, str) and 'errors' in result:
                log.result = result
            else:
                # Maybe returns a Queryset or an Object and it's ok 200
                log.result = '[200] OK'

            log.save()
        except db.ValidationError as e:
            # print 'Something went wrong in the log', e
            pass