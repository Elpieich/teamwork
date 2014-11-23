    # items = db.ListField(db.ReferenceField('Item'))
    # discount = db.FloatField()
    # start_date = db.DateTimeField()
    # end_date = db.DateTimeField()
    # accepted = db.BooleanField(default=False)
    # comments = db.StringField(max_length=255)

import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class OfferTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()

#
#    OFFER
#   -----------
#
    def test_offers(self):
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.offer_id = str(json_data["_id"]["$oid"])
        expected_json = "{u'items': [], u'accepted': False, u'_id': {u'$oid': u'%s'}}" % self.offer_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)
        self.offer_detail()

    def offer_detail(self):
        response = self.app.get('/offers/%s?auth_token=%s' % (self.offer_id, token), content_type='application/json')
        expected_json = "{u'items': [], u'accepted': False, u'_id': {u'$oid': u'%s'}}" % self.offer_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.offer_update()

    def offer_update(self):
        accepted = True
        response = self.app.put('/offers/%s' % self.offer_id,
            data=json.dumps(dict(
                auth_token=token,
                accepted=accepted
                )),
            content_type='application/json')
        expected_json = "{u'items': [], u'accepted': True, u'_id': {u'$oid': u'%s'}}" % self.offer_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.offer_delete()

    def offer_delete(self):
        response = self.app.delete('/offers/%s' % self.offer_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_offers_search(self):
        response = self.app.get('/offers/search?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()