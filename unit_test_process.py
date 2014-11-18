import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class ProcessTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.get_app().test_client()

#    def test(self):
#        response = self.app.get('/', content_type='application/json')
#        self.assertEqual(response.data, '{\n  "error": "Not found"\n}')

#
#    PROCESSES
#   -----------
#
    def test_processes(self):
        response = self.app.get('/processes?auth_token=' + token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process(self):
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
        expected_json = "{u'stages': [], u'_id': {u'$oid': u'%s'}, u'name': u'Venta de Unittest', u'description': u'Proceso para la venta de unittest'}" % self.process_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_data), expected_json)
        self.process_detail()

    def process_detail(self):
        response = self.app.get('/processes/%s?auth_token=%s' % (self.process_id, token), content_type='application/json')
        expected_json = "{u'stages': [], u'_id': {u'$oid': u'%s'}, u'name': u'Venta de Unittest', u'description': u'Proceso para la venta de unittest'}" % self.process_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.process_update()

    def process_update(self):
        name = "Venta de hamburguesas"
        description = "Proceso para la venta de hamburguesas"
        response = self.app.put('/processes/%s' % self.process_id,
            data=json.dumps(dict(
                auth_token=token,
                name=name,
                description=description 
                )),
            content_type='application/json')
        expected_json = "{u'stages': [], u'_id': {u'$oid': u'%s'}, u'name': u'Venta de hamburguesas', u'description': u'Proceso para la venta de hamburguesas'}" % self.process_id
        json_data = json.loads(response.data)
        self.assertEqual(str(json_data), expected_json)
        self.assertEqual(response.status_code, 200)
        self.process_delete()

    def process_delete(self):
        response = self.app.delete('/processes/%s' % self.process_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_processes_search(self):
        response = self.app.get('/processes/search?auth_token=%s' % token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()