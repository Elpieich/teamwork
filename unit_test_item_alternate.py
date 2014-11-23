#    name
#    description
#    price = db.FloatField(default=0.0)

import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class ItemAlternateTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()
        self.fake_item_id = "0123456789qwertyuiopasdf"
        
        #create dummy item
        name = "Chocolate"
        description = "Chocolate delicioso."
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=token,
                name=name,
                description=description 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.item_id = str(json_data["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        response = self.app.delete('/item/%s' % self.item_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    ITEM
#   -----------
#
    def test_create_no_fields(self):
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=token,
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.item_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}}" % self.item_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)

    def test_create_no_name(self):
        description = "Chocolate delicioso."
        price = 10.0
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=token,
                description=description,
                price=price 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.item_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'price': 10.0, u'_id': {u'$oid': u'%s'}, u'description': u'Chocolate delicioso.'}" % self.item_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)

    def test_create_no_description(self):
        name = "Chocolate"
        price = 10.0
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=token,
                name=name,
                price=price
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.item_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'price': 10.0, u'_id': {u'$oid': u'%s'}, u'name': u'Chocolate'}" % self.item_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)

    def test_create_no_price(self):
        name = "Chocolate"
        description = "Chocolate delicioso."
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=token,
                name=name,
                description=description
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.item_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'name': u'Chocolate', u'description': u'Chocolate delicioso.'}" % self.item_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)

    def test_id_null(self):
        response = self.app.get('/items/%s?auth_token=%s' % (self.fake_item_id, token), content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_update(self):
        self.update_no_fields()
        self.update_no_name()
        self.update_no_description()
        self.update_price()

    def update_no_fields(self):
        response = self.app.put('/items/%s' % self.item_id,
            data=json.dumps(dict(
                auth_token=token,
                )),
            content_type='application/json')
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'name': u'Chocolate', u'description': u'Chocolate delicioso.'}" % self.item_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)

    def update_no_name(self):
        description = "Chocolate muy delicioso"
        response = self.app.put('/items/%s' % self.item_id,
            data=json.dumps(dict(
                auth_token=token,
                description=description
                )),
            content_type='application/json')
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'name': u'Chocolate', u'description': u'Chocolate muy delicioso'}" % self.item_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)

    def update_no_description(self):
        name = "Chocolate blanco"
        response = self.app.put('/items/%s' % self.item_id,
            data=json.dumps(dict(
                auth_token=token,
                name=name
                )),
            content_type='application/json')
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'name': u'Chocolate blanco', u'description': u'Chocolate muy delicioso'}" % self.item_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)

    def update_price(self):
        price = 100.0
        response = self.app.put('/items/%s' % self.item_id,
            data=json.dumps(dict(
                auth_token=token,
                price=price
                )),
            content_type='application/json')
        expected_json = "{u'price': 100.0, u'_id': {u'$oid': u'%s'}, u'name': u'Chocolate blanco', u'description': u'Chocolate muy delicioso'}" % self.item_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        
    def test_item_delete(self):
        response = self.app.delete('/item/%s' % self.fake_item_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)


if __name__ == '__main__':
    unittest.main()