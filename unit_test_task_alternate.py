import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class TaskAlternateTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()

        self.description_overflow = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce malesuada ornare risus vel pretium. Donec consectetur a nunc vitae dictum. Lorem ipsum dolor sit amet."
        self.fake_task_id = "0123456789qwertyuiopasdf"

        # create dummy task
        description = "Task Unittest"
        response = self.app.post('/tasks',
            data=json.dumps(dict(
                auth_token=token,
                description=description
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.task_id = str(json_data["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        response = self.app.delete('/tasks/%s' % self.task_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    TASKS
#   -----------
#
    def test_create_description_overflow(self):
        response = self.app.post('/tasks',
            data=json.dumps(dict(
                auth_token=token,
                description=self.description_overflow 
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_create_no_fields(self):
        response = self.app.post('/tasks',
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)


    def test_id_null(self):
        response = self.app.get('/tasks/%s?auth_token=%s' % (self.fake_task_id, token), content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_update(self):
        self.update_no_fields()

    def update_no_fields(self):
        response = self.app.put('/tasks/%s' % self.task_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        expected_json = "{u'completed': False, u'_id': {u'$oid': u'%s'}, u'description': u'Task Unittest'}" % self.task_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
 

    def test_task_delete(self):
        response = self.app.delete('/tasks/%s' % self.fake_task_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)  


if __name__ == '__main__':
    unittest.main()