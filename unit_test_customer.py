    # sales = db.ListField(db.ReferenceField('Sale'))
    # business_name = db.StringField(max_length=140)
    # rfc = db.StringField(max_length=13, min_length=10, unique=True)

import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class CustomerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()
        self.rfc = "ROPL951200"

#
#    CUSTOMER
#   -----------
#

    def test_get_customers(self):
        response = self.app.get('/customers?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_customers(self):
        business_name="Business corp."
        response = self.app.post('/customers',
            data=json.dumps(dict(
                auth_token=token,
                business_name=business_name,
                rfc=self.rfc
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.customer_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'rfc': u'%s', u'business_name': u'Business corp.', u'_id': {u'$oid': u'%s'}, u'sales': []}" % (self.rfc, self.customer_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)
        self.customer_detail()

    def customer_detail(self):
        response = self.app.get('/customers/%s?auth_token=%s' % (self.customer_id, token), content_type='application/json')
        expected_json = "{u'rfc': u'%s', u'business_name': u'Business corp.', u'_id': {u'$oid': u'%s'}, u'sales': []}" % (self.rfc, self.customer_id)
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.customer_update()

    def customer_update(self):
        business_name = "Business Update"
        response = self.app.put('/customers/%s' % self.customer_id,
            data=json.dumps(dict(
                auth_token=token,
                business_name=business_name
                )),
            content_type='application/json')
        expected_json = "{u'rfc': u'%s', u'business_name': u'Business Update', u'_id': {u'$oid': u'%s'}, u'sales': []}" % (self.rfc, self.customer_id)
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.customer_delete()

    def customer_delete(self):
        response = self.app.delete('/customers/%s' % self.customer_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_customers_search(self):
        response = self.app.get('/customers/search?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()