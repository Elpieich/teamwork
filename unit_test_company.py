    # name = db.StringField(required=True, min_length=1, max_length=140)
    # direction = db.StringField(required=True, min_length=1, max_length=140)
    # admin = db.ReferenceField('User')

import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class CompanyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()
        self.name = "Hola Inc."
        self.direction = "Direccion hol aloha"

#
#    COMPANY
#   -----------
#

    def test_get_companies(self):
        response = self.app.get('/companies?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_companies(self):
        response = self.app.post('/companies',
            data=json.dumps(dict(
                auth_token=token,
                name=self.name,
                direction=self.direction
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.company_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'direction': u'%s', u'_id': {u'$oid': u'%s'}, u'name': u'%s'}" % (self.direction, self.company_id, self.name)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)
        self.company_detail()

    def company_detail(self):
        response = self.app.get('/companies/%s?auth_token=%s' % (self.company_id, token), content_type='application/json')
        expected_json = "{u'direction': u'%s', u'_id': {u'$oid': u'%s'}, u'name': u'%s'}" % (self.direction, self.company_id, self.name)
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.company_update()

    def company_update(self):
        name = "Hola Update"
        response = self.app.put('/companies/%s' % self.company_id,
            data=json.dumps(dict(
                auth_token=token,
                name=name
                )),
            content_type='application/json')
        expected_json = "{u'direction': u'%s', u'_id': {u'$oid': u'%s'}, u'name': u'%s'}" % (self.direction, self.company_id, name)
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.company_delete()

    def company_delete(self):
        response = self.app.delete('/companies/%s' % self.company_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_companys_search(self):
        response = self.app.get('/companies/search?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()