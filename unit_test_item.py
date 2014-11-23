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

class ItemTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()

#
#    ITEM
#   -----------
#
    def test_items(self):
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.item_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}}" % self.item_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)
        self.item_detail()

    def item_detail(self):
        response = self.app.get('/items/%s?auth_token=%s' % (self.item_id, token), content_type='application/json')
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}}" % self.item_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.item_update()

    def item_update(self):
        description = "Item Update"
        response = self.app.put('/items/%s' % self.item_id,
            data=json.dumps(dict(
                auth_token=token,
                description=description
                )),
            content_type='application/json')
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'description': u'Item Update'}" % self.item_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.item_delete()

    def item_delete(self):
        response = self.app.delete('/item/%s' % self.item_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_items_search(self):
        response = self.app.get('/items/search?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()