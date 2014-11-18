import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class StageTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()

        self.name_overflow = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.description_overflow = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce malesuada ornare risus vel pretium. Donec consectetur a nunc vitae dictum. Lorem ipsum dolor sit amet."
        self.fake_stage_id = "0123456789qwertyuiopasdf"

        # create dummy process
        name = "Stage Unittest"
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=token,
                name=name
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.stage_id = str(json_data["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        response = self.app.delete('/stages/%s' % self.stage_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    STAGES
#   -----------
#
    def test_create_name_overflow(self):
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=token,
                name=self.name_overflow 
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_create_description_overflow(self):
        name = "Stage Unittest"
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=token,
                name=name,
                description=self.description_overflow 
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_create_no_fields(self):
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_create_no_name(self):
        description = "Stage description"
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=token,
                description=description
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_id_null(self):
        response = self.app.get('/stages/%s?auth_token=%s' % (self.fake_stage_id, token), content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_update(self):
        self.update_no_fields()
        self.update_no_description()
        self.update_no_name()

    def update_no_fields(self):
        response = self.app.put('/stages/%s' % self.stage_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        expected_json = "{u'tasks': [], u'_id': {u'$oid': u'%s'}, u'name': u'Stage Unittest'}" % self.stage_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)

    def update_no_description(self):
        name = "Stage Update"
        response = self.app.put('/stages/%s' % self.stage_id,
            data=json.dumps(dict(
                auth_token=token,
                name=name
                )),
            content_type='application/json')
        expected_json = "{u'tasks': [], u'_id': {u'$oid': u'%s'}, u'name': u'Stage Update'}" % self.stage_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)

    def update_no_name(self):
        description = "Stage description"
        response = self.app.put('/stages/%s' % self.stage_id,
            data=json.dumps(dict(
                auth_token=token,
                description=description
                )),
            content_type='application/json')
        expected_json = "{u'tasks': [], u'_id': {u'$oid': u'%s'}, u'name': u'Stage Update', u'description': u'Stage description'}" % self.stage_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)  

    def test_stage_delete(self):
        response = self.app.delete('/stages/%s' % self.fake_stage_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)  


if __name__ == '__main__':
    unittest.main()