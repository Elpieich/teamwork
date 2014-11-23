    # customer = db.ReferenceField('Customer')
    # owner = db.ReferenceField('Member')
    # process = db.ReferenceField('Process')
    # status = db.StringField(choices=STATUS)
    # sales = db.ListField(db.ReferenceField('sale'))
    # team = db.ReferenceField('Team')

import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class SaleTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()

#
#    SALE
#   -----------
#
    def test_get_sales(self):
        response = self.app.get('/sales?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_sales(self):
        response = self.app.post('/sales',
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.sale_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'items': [], u'accepted': False, u'_id': {u'$oid': u'%s'}}" % self.sale_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)
        self.sale_detail()

    def sale_detail(self):
        response = self.app.get('/sales/%s?auth_token=%s' % (self.sale_id, token), content_type='application/json')
        expected_json = "{u'items': [], u'accepted': False, u'_id': {u'$oid': u'%s'}}" % self.sale_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.sale_update()

    def sale_update(self):
        accepted = True
        response = self.app.put('/sales/%s' % self.sale_id,
            data=json.dumps(dict(
                auth_token=token,
                accepted=accepted
                )),
            content_type='application/json')
        expected_json = "{u'items': [], u'accepted': True, u'_id': {u'$oid': u'%s'}}" % self.sale_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.sale_delete()

    def sale_delete(self):
        response = self.app.delete('/sales/%s' % self.sale_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_sales_search(self):
        response = self.app.get('/sales/search?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()