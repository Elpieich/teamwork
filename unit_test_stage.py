    # name = db.StringField(max_length=40, required=True)
    # description = db.StringField(max_length=140)
    # template = db.ReferenceField('StageTemplate')
    # process = db.ReferenceField('Process')
    # template = db.ReferenceField('StageTemplate')
    # manager = db.ReferenceField('User')
    # status = db.ReferenceField('StageStatus')
    # tasks = db.ListField(db.ReferenceField('Task'))

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

#
#    STAGES
#   -----------
#
    def test_stages(self):
        name = "Stage Unittest"
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=token,
                name=name 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.stage_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'tasks': [], u'_id': {u'$oid': u'%s'}, u'name': u'Stage Unittest'}" % self.stage_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)
        self.stage_detail()

    def stage_detail(self):
        response = self.app.get('/stages/%s?auth_token=%s' % (self.stage_id, token), content_type='application/json')
        expected_json = "{u'tasks': [], u'_id': {u'$oid': u'%s'}, u'name': u'Stage Unittest'}" % self.stage_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.stage_update()

    def stage_update(self):
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
        self.stage_delete()

    def stage_delete(self):
        response = self.app.delete('/stages/%s' % self.stage_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_stages_search(self):
        response = self.app.get('/stages/search?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()