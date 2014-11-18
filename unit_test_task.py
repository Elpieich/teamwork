    # description = db.StringField(max_length=140, required=True)
    # task = db.ReferenceField('task')
    # completed = db.BooleanField(default=False)
    # owner = db.ReferenceField('User')
    # manager = db.ReferenceField('User')
    # progress = db.IntField(max_value=100, min_value=0)

import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class TaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()

#
#    TASKS
#   -----------
#
    def test_tasks(self):
        description = "Task Unittest"
        response = self.app.post('/tasks',
            data=json.dumps(dict(
                auth_token=token,
                description=description 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.task_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'completed': False, u'_id': {u'$oid': u'%s'}, u'description': u'Task Unittest'}" % self.task_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)
        self.task_detail()

    def task_detail(self):
        response = self.app.get('/tasks/%s?auth_token=%s' % (self.task_id, token), content_type='application/json')
        expected_json = "{u'completed': False, u'_id': {u'$oid': u'%s'}, u'description': u'Task Unittest'}" % self.task_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.task_update()

    def task_update(self):
        description = "Task Update"
        response = self.app.put('/tasks/%s' % self.task_id,
            data=json.dumps(dict(
                auth_token=token,
                description=description
                )),
            content_type='application/json')
        expected_json = "{u'completed': False, u'_id': {u'$oid': u'%s'}, u'description': u'Task Update'}" % self.task_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.task_delete()

    def task_delete(self):
        response = self.app.delete('/tasks/%s' % self.task_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_tasks_search(self):
        response = self.app.get('/tasks/search?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()