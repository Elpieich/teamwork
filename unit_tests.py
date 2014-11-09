import os
import json
import unittest
import tempfile

from crm.apps.api import API

api = API()

token = 'WyI1NDUyZTEzYTE2Yzc3YTAzZmY3NTc2YTAiLCJlZjI4YWFmN2FjOTUzMjNhOWFkZDcxMzk0MmYyM2NiMSJd.BzXvZg.ySdSQnVK4NHWIe_Yx0sBDe6JIU0'

class FlaskTestCase(unittest.TestCase):
    process_id = ""

    def setUp(self):
        self.app = api.get_app().test_client()

    def test(self):
        response = self.app.get('/', content_type='application/json')
        self.assertEqual(response.data, '{\n  "error": "Not found"\n}')

#
#    PROCESSES
#   -----------
#
    def test_processes(self):
        response = self.app.get('/processes?auth_token=' + token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process_create(self):
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

    def test_process_detail(self):
        print "process_id =" + self.process_id
        response = self.app.get('/processes/%s?auth_token=%s' % (self.process_id, token), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process_update(self):
        print "process_id =" + self.process_id
        name = "Venta de hamburguesas"
        description = "Proceso para la venta de hamburguesas"
        response = self.app.put('/processes/%s' % self.process_id,
            data=json.dumps(dict(
                auth_token=token,
                name=name,
                description=description 
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process_delete(self):
        print "process_id =" + self.process_id
        response = self.app.delete('/processes/%s' % self.process_id,
            data=json.dumps(dict(
                auth_token=token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()