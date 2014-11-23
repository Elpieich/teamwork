    # name = db.StringField(max_length=140)
    # members = db.ListField(db.ReferenceField('Member'))
    # leader = db.ReferenceField('Member')
    # sales = db.ListField(db.ReferenceField('Sale'))

import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class TeamTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()

#
#    TEAM
#   -----------
#

    def test_get_teams(self):
        response = self.app.get('/teams?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_teams(self):
        response = self.app.post('/teams',
            data=json.dumps(dict(
                auth_token=token,
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.team_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'_id': {u'$oid': u'%s'}, u'sales': [], u'members': []}" % self.team_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)
        self.team_detail()

    def team_detail(self):
        response = self.app.get('/teams/%s?auth_token=%s' % (self.team_id, token), content_type='application/json')
        expected_json = "{u'_id': {u'$oid': u'%s'}, u'sales': [], u'members': []}" % self.team_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.team_update()

    def team_update(self):
        business_name = "Business Update"
        response = self.app.put('/teams/%s' % self.team_id,
            data=json.dumps(dict(
                auth_token=token,
                business_name=business_name
                )),
            content_type='application/json')
        expected_json = "{u'_id': {u'$oid': u'%s'}, u'sales': [], u'members': []}" % self.team_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.team_delete()

    def team_delete(self):
        response = self.app.delete('/teams/%s' % self.team_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_teams_search(self):
        response = self.app.get('/teams/search?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()