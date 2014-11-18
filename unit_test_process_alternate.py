import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class ProcessAlternateTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()
        self.name_overflow = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.description_overflow = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce malesuada ornare risus vel pretium. Donec consectetur a nunc vitae dictum. Lorem ipsum dolor sit amet."
        self.fake_process_id = "546a9e54efe85d2d48fa0392"
        #create dummy process
        name = "Venta de Unittest"
        description = "Proceso para la venta de unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=token,
                name=name,
                description=description 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        self.process_id = str(json_data["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        response = self.app.delete('/processes/%s' % self.process_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    PROCESSES
#   -----------
#
    def test_create_name_overflow(self):
        description = "Proceso para la venta de unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=token,
                name=self.name_overflow,
                description=description 
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_create_decription_overflow(self):
        name = "Venta de Unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=token,
                name=name,
                description=self.description_overflow
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_create_no_name_no_description(self):
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=token,
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_create_no_description(self):
        name = "Venta de Unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=token,
                name=name,
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_create_no_name(self):
        description = "Proceso para la venta de unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=token,
                description=description 
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_detail_null(self):
        response = self.app.get('/processes/%s?auth_token=%s' % (self.fake_process_id, token), content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_update(self):
        self.process_update_no_fields()
        self.process_update_no_description()
        self.process_update_no_name()

    def process_update_no_fields(self):
        response = self.app.put('/processes/%s' % self.process_id,
            data=json.dumps(dict(
                auth_token=token,
                )),
            content_type='application/json')
        expected_json = "{u'stages': [], u'_id': {u'$oid': u'%s'}, u'name': u'Venta de Unittest', u'description': u'Proceso para la venta de unittest'}" % self.process_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)

    def process_update_no_description(self):
        name = "Venta de hamburguesas con queso"
        response = self.app.put('/processes/%s' % self.process_id,
            data=json.dumps(dict(
                auth_token=token,
                name=name
                )),
            content_type='application/json')
        expected_json = "{u'stages': [], u'_id': {u'$oid': u'%s'}, u'name': u'Venta de hamburguesas con queso', u'description': u'Proceso para la venta de unittest'}" % self.process_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)

    def process_update_no_name(self):
        description = "Proceso para la venta de hamburguesas"
        response = self.app.put('/processes/%s' % self.process_id,
            data=json.dumps(dict(
                auth_token=token,
                description=description
                )),
            content_type='application/json')
        expected_json = "{u'stages': [], u'_id': {u'$oid': u'%s'}, u'name': u'Venta de hamburguesas con queso', u'description': u'Proceso para la venta de hamburguesas'}" % self.process_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        


if __name__ == '__main__':
    unittest.main()