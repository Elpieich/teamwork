import os
import json
import unittest
import tempfile
import datetime
import calendar

from crm.apps.api import API

api = API()

class AllTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.app.test_client()
        self.username = "ricardo.ivan91@gmail.com"
        self.password = "WyJXeUpPY"
        self.owner = "547144128d9912494ea0274e"
        self.token = 'WyI1NDcxNDQxMjhkOTkxMjQ5NGVhMDI3NGQiLCJkOWI0MDM3M2ZhZGM4OTAwMDAwYjU2NDljNjZmNWQ1NCJd.B1ga-Q.rBKeHcVI_c422l8NVSKHcA7FIj8'

        self.name_overflow = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.description_overflow = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce malesuada ornare risus vel pretium. Donec consectetur a nunc vitae dictum. Lorem ipsum dolor sit amet."
        self.fake_id = "0123456789qwertyuiopasdf"
        self.rfc = "ROPL951201"


    def tearDown(self):
        pass

    def json_string(self, response):
        response = str(response).replace("'{", '{')
        response = str(response).replace("}'", '}')
        response = str(response).replace("'", '"')
        response = str(response).replace(": u", ': ')
        return response

#
#    LOGIN
#   -----------
#

    def test_auth(self):
        response = self.app.post('/auth',
            data=json.dumps(dict(
                email=self.username,
                password=self.password
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    PROCESSES
#   -----------
#
    # def test_processes(self):
    #     response = self.app.get('/processes?auth_token=' + self.token, content_type='application/json')
    #     self.assertEqual(response.status_code, 200)

    def create_dummy_process(self):
        #create process
        name = "Venta de Unittest"
        description = "Proceso para la venta de unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                description=description 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        proceso = str(json_d["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)
        return proceso

    def delete_dummy_process(self, proceso):
        response = self.app.delete('/processes/%s' % proceso,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process(self):
        name = "Venta de Unittest"
        description = "Proceso para la venta de unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                description=description 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        proceso = str(json_d["_id"]["$oid"])
        expected_json = "{u'stages': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Venta de Unittest', u'description': u'Proceso para la venta de unittest'}" % (self.owner, proceso)
        self.assertEqual(json_data["status"], 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_process(proceso)

    def test_process_detail(self):
        proceso = self.create_dummy_process()
        response = self.app.get('/processes/%s?auth_token=%s' % (proceso, self.token), content_type='application/json')
        expected_json = "{u'stages': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Venta de Unittest', u'description': u'Proceso para la venta de unittest'}" % (self.owner, proceso)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_process(proceso)

    def test_process_update(self):
        proceso = self.create_dummy_process()
        name = "Venta de hamburguesas"
        description = "Proceso para la venta de hamburguesas"
        response = self.app.put('/processes/%s' % proceso,
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                description=description 
                )),
            content_type='application/json')
        expected_json = "{u'stages': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Venta de hamburguesas', u'description': u'Proceso para la venta de hamburguesas'}" % (self.owner, proceso)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_process(proceso)

    def test_process_delete(self):
        proceso = self.create_dummy_process()
        response = self.app.delete('/processes/%s' % proceso,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_processes_search(self):
        response = self.app.get('/processes/search?auth_token=%s' % self.token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process_create_name_overflow(self):
        description = "Proceso para la venta de unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=self.token,
                name=self.name_overflow,
                description=description 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(response.status_code, 200)

    def test_process_create_decription_overflow(self):
        name = "Venta de Unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                description=self.description_overflow
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process_create_no_fields(self):
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=self.token,
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process_create_no_description(self):
        name = "Venta de Unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process_create_no_name(self):
        description = "Proceso para la venta de unittest"
        response = self.app.post('/processes',
            data=json.dumps(dict(
                auth_token=self.token,
                description=description 
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process_id_null(self):
        response = self.app.get('/processes/%s?auth_token=%s' % (self.fake_id, self.token), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_process_update_no_fields(self):
        proceso = self.create_dummy_process()
        response = self.app.put('/processes/%s' % proceso,
            data=json.dumps(dict(
                auth_token=self.token,
                )),
            content_type='application/json')
        expected_json = "{u'stages': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Venta de Unittest', u'description': u'Proceso para la venta de unittest'}" % (self.owner, proceso)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_process(proceso)

    def test_process_update_no_description(self):
        proceso = self.create_dummy_process()
        name = "Venta de hamburguesas con queso"
        response = self.app.put('/processes/%s' % proceso,
            data=json.dumps(dict(
                auth_token=self.token,
                name=name
                )),
            content_type='application/json')
        expected_json = "{u'stages': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Venta de hamburguesas con queso', u'description': u'Proceso para la venta de unittest'}" % (self.owner, proceso)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_process(proceso)

    def process_update_no_name(self):
        proceso = self.create_dummy_process()
        description = "Proceso para la venta de hamburguesas"
        response = self.app.put('/processes/%s' % proceso,
            data=json.dumps(dict(
                auth_token=self.token,
                description=description
                )),
            content_type='application/json')
        expected_json = "{u'stages': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Venta de hamburguesas con queso', u'description': u'Proceso para la venta de hamburguesas'}" % (self.owner, proceso)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_process(proceso)
        
    def test_process_delete(self):
        response = self.app.delete('/processes/%s' % self.fake_id,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    STAGES
#   -----------
#

    def create_dummy_stage(self,):
        # create dummy stage
        name = "Stage Unittest"
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        stage = str(json_d["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)
        return stage

    def delete_dummy_stage(self, stage):
        response = self.app.delete('/stages/%s' % stage,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_stages(self):
        name = "Stage Unittest"
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        stage = str(json_d["_id"]["$oid"])
        expected_json = "{u'tasks': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Stage Unittest'}" % (self.owner, stage)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_stage(stage)

    def test_stage_detail(self):
        stage = self.create_dummy_stage()
        response = self.app.get('/stages/%s?auth_token=%s' % (stage, self.token), content_type='application/json')
        expected_json = "{u'tasks': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Stage Unittest'}" % (self.owner, stage)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_stage(stage)

    def test_stage_update(self):
        stage = self.create_dummy_stage()
        name = "Stage Update"
        response = self.app.put('/stages/%s' % stage,
            data=json.dumps(dict(
                auth_token=self.token,
                name=name
                )),
            content_type='application/json')
        expected_json = "{u'tasks': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Stage Update'}" % (self.owner, stage)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_stage(stage)

    def stage_delete(self, stage):
        stage = self.create_dummy_stage()
        response = self.app.delete('/stages/%s' % stage,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_stages_search(self):
        response = self.app.get('/stages/search?auth_token=%s' % self.token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_stage_create_name_overflow(self):
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=self.token,
                name=self.name_overflow 
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_stage_create_description_overflow(self):
        name = "Stage Unittest"
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                description=self.description_overflow 
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_stage_create_no_fields(self):
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_stage_create_no_name(self):
        description = "Stage description"
        response = self.app.post('/stages',
            data=json.dumps(dict(
                auth_token=self.token,
                description=description
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_stage_id_null(self):
        response = self.app.get('/stages/%s?auth_token=%s' % (self.fake_id, self.token), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_stage_update_no_fields(self):
        stage = self.create_dummy_stage()
        response = self.app.put('/stages/%s' % stage,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        expected_json = "{u'tasks': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Stage Unittest'}" % (self.owner, stage)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_stage(stage)

    def test_stage_update_no_description(self):
        stage = self.create_dummy_stage()
        name = "Stage Update"
        response = self.app.put('/stages/%s' % stage,
            data=json.dumps(dict(
                auth_token=self.token,
                name=name
                )),
            content_type='application/json')
        expected_json = "{u'tasks': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Stage Update'}" % (self.owner, stage)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_stage(stage)

    def test_stage_update_no_name(self):
        stage = self.create_dummy_stage()
        description = "Stage description"
        response = self.app.put('/stages/%s' % stage,
            data=json.dumps(dict(
                auth_token=self.token,
                description=description
                )),
            content_type='application/json')
        expected_json = "{u'tasks': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'name': u'Stage Unittest', u'description': u'Stage description'}" % (self.owner, stage)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200) 
        self.delete_dummy_stage(stage) 

    def test_stage_delete(self):
        response = self.app.delete('/stages/%s' % self.fake_id,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    TASKS
#   -----------
#

    def create_dummy_task(self):
        # create dummy task
        description = "Task Unittest"
        response = self.app.post('/tasks',
            data=json.dumps(dict(
                auth_token=self.token,
                description=description
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        task = str(json_d["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)
        return task

    def delete_dummy_task(self, task):
        response = self.app.delete('/tasks/%s' % task,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_tasks(self):
        description = "Task Unittest"
        response = self.app.post('/tasks',
            data=json.dumps(dict(
                auth_token=self.token,
                description=description 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        task = str(json_d["_id"]["$oid"])
        expected_json = "{u'completed': False, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'description': u'Task Unittest'}"% (task, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_task(task)

    def test_task_detail(self):
        task = self.create_dummy_task()
        response = self.app.get('/tasks/%s?auth_token=%s' % (task, self.token), content_type='application/json')
        expected_json = "{u'completed': False, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'description': u'Task Unittest'}"% (task, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_task(task)


    def test_task_update(self):
        task = self.create_dummy_task()
        description = "Task Update"
        response = self.app.put('/tasks/%s' % task,
            data=json.dumps(dict(
                auth_token=self.token,
                description=description
                )),
            content_type='application/json')
        expected_json = "{u'completed': False, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'description': u'Task Update'}"% (task, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_task(task)


    def test_task_delete(self):
        task = self.create_dummy_task()
        response = self.app.delete('/tasks/%s' % task,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_tasks_search(self):
        response = self.app.get('/tasks/search?auth_token=%s' % self.token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_task_create_description_overflow(self):
        response = self.app.post('/tasks',
            data=json.dumps(dict(
                auth_token=self.token,
                description=self.description_overflow 
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_task_create_no_fields(self):
        response = self.app.post('/tasks',
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_task_id_null(self):
        response = self.app.get('/tasks/%s?auth_token=%s' % (self.fake_id, self.token), content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_task_update_no_fields(self):
        task = self.create_dummy_task()
        response = self.app.put('/tasks/%s' % task,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        expected_json = "{u'completed': False, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'description': u'Task Unittest'}"% (task, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_task(task)

    def test_task_delete(self):
        response = self.app.delete('/tasks/%s' % self.fake_id,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    ITEM
#   -----------
#

    def create_dummy_item(self):
        #create dummy item
        name = "Chocolate"
        description = "Chocolate delicioso."
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                description=description 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        item = str(json_d["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)
        return item

    def delete_dummy_item(self, item):
        response = self.app.delete('/item/%s' % item,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_items(self):
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        item = str(json_d["_id"]["$oid"])
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}}"% (item, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_item(item)
        

    def test_item_detail(self):
        item = self.create_dummy_item()
        response = self.app.get('/items/%s?auth_token=%s' % (item, self.token), content_type='application/json')
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'name': u'Chocolate', u'description': u'Chocolate delicioso.'}"% (item, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_item(item)

    def test_item_update(self):
        item = self.create_dummy_item()
        description = "Item Update"
        response = self.app.put('/items/%s' % item,
            data=json.dumps(dict(
                auth_token=self.token,
                description=description
                )),
            content_type='application/json')
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'name': u'Chocolate', u'description': u'Item Update'}"% (item, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_item(item)

    def test_item_delete(self):
        item = self.create_dummy_item()
        response = self.app.delete('/item/%s' % item,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_items_search(self):
        response = self.app.get('/items/search?auth_token=%s' % self.token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_item_create_no_fields(self):
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=self.token,
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        item = str(json_d["_id"]["$oid"])
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}}"% (item, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_item(item)

    def test_item_create_no_name(self):
        description = "Chocolate delicioso."
        price = 10.0
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=self.token,
                description=description,
                price=price 
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        item = str(json_d["_id"]["$oid"])
        expected_json = "{u'price': 10.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'description': u'Chocolate delicioso.'}"% (item, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_item(item)

    def test_item_create_no_description(self):
        name = "Chocolate"
        price = 10.0
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                price=price
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        item = str(json_d["_id"]["$oid"])
        expected_json = "{u'price': 10.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'name': u'Chocolate'}"% (item, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_item(item)

    def test_item_create_no_price(self):
        name = "Chocolate"
        description = "Chocolate delicioso."
        response = self.app.post('/items',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                description=description
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        item = str(json_d["_id"]["$oid"])
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'name': u'Chocolate', u'description': u'Chocolate delicioso.'}"% (item, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_item(item)

    def test_item_id_null(self):
        response = self.app.get('/items/%s?auth_token=%s' % (self.fake_id, self.token), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_item_update_no_fields(self):
        item = self.create_dummy_item()
        response = self.app.put('/items/%s' % item,
            data=json.dumps(dict(
                auth_token=self.token,
                )),
            content_type='application/json')
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'name': u'Chocolate', u'description': u'Chocolate delicioso.'}"% (item, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_item(item)

    def test_item_update_no_name(self):
        item = self.create_dummy_item()
        description = "Chocolate muy delicioso"
        response = self.app.put('/items/%s' % item,
            data=json.dumps(dict(
                auth_token=self.token,
                description=description
                )),
            content_type='application/json')
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'name': u'Chocolate', u'description': u'Chocolate muy delicioso'}"% (item, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_item(item)

    def test_item_update_no_description(self):
        item = self.create_dummy_item()
        name = "Chocolate blanco"
        response = self.app.put('/items/%s' % item,
            data=json.dumps(dict(
                auth_token=self.token,
                name=name
                )),
            content_type='application/json')
        expected_json = "{u'price': 0.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'name': u'Chocolate blanco', u'description': u'Chocolate delicioso.'}"% (item, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_item(item)

    def test_item_update_price(self):
        item = self.create_dummy_item()
        price = 100.0
        response = self.app.put('/items/%s' % item,
            data=json.dumps(dict(
                auth_token=self.token,
                price=price
                )),
            content_type='application/json')
        expected_json = "{u'price': 100.0, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'name': u'Chocolate', u'description': u'Chocolate delicioso.'}"% (item, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_item(item)
        
    def test_item_delete(self):
        response = self.app.delete('/item/%s' % self.fake_id,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    OFFER
#   -----------
#
    def create_dummy_offer(self):
        # create dummy offer
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)
        return offer

    def delete_dummy_offer(self, offer):
        response = self.app.delete('/offers/%s' % offer,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_offers(self):
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        expected_json = "{u'items': [], u'accepted': False, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}}" % (offer, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_offer(offer)

    def test_offer_detail(self):
        offer = self.create_dummy_offer()
        response = self.app.get('/offers/%s?auth_token=%s' % (offer, self.token), content_type='application/json')
        expected_json = "{u'items': [], u'accepted': False, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}}" % (offer, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_offer(offer)

    def test_offer_update(self):
        offer = self.create_dummy_offer()
        accepted = True
        response = self.app.put('/offers/%s' % offer,
            data=json.dumps(dict(
                auth_token=self.token,
                accepted=accepted
                )),
            content_type='application/json')
        expected_json = "{u'items': [], u'accepted': True, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}}" % (offer, self.owner)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_offer(offer)

    def test_offer_delete(self):
        offer = self.create_dummy_offer()
        response = self.app.delete('/offers/%s' % offer,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_offers_search(self):
        response = self.app.get('/offers/search?auth_token=%s' % self.token, content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_create_discount(self):
        discount = 0.0
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        expected_json = "{u'items': [], u'accepted': False, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'discount': 0.0}" % (offer, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_offer(offer)

    def test_create_discount_start_date(self):
        discount = 0.0
        start_date = datetime.datetime.now()
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                start_date=str(start_date)
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_start_date_end_date(self):
        discount = 0.0
        start_date = datetime.datetime.now()
        end_date = datetime.datetime.now()
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                start_date=str(start_date),
                end_date=str(end_date)
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_start_date_accepted(self):
        discount = 0.0
        start_date = datetime.datetime.now()
        accepted = True
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                start_date=str(start_date),
                accepted=True
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_start_date_comments(self):
        discount = 0.0
        comments = "Comentario"
        start_date = datetime.datetime.now()
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                comments=comments,
                start_date=str(start_date)
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_start_date_end_date_accepted(self):
        discount = 0.0
        start_date = datetime.datetime.now()
        end_date = datetime.datetime.now()
        accepted = True
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                start_date=str(start_date),
                end_date=str(end_date),
                accepted=accepted
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_start_date_end_date_comments(self):
        discount = 0.0
        start_date = datetime.datetime.now()
        end_date = datetime.datetime.now()
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                start_date=str(start_date),
                end_date=str(end_date),
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_start_date_accepted_comments(self):
        discount = 0.0
        start_date = datetime.datetime.now()
        accepted = True
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                start_date=str(start_date),
                accepted=True,
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_end_date(self):
        discount = 0.0
        end_date = datetime.datetime.now()
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                end_date=str(end_date)
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_end_date_accepted(self):
        discount = 0.0
        end_date = datetime.datetime.now()
        accepted = True
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                end_date=str(end_date),
                accepted=True
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_end_date_comments(self):
        discount = 0.0
        end_date = datetime.datetime.now()
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                end_date=str(end_date),
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_end_date_accepted_comments(self):
        discount = 0.0
        end_date = datetime.datetime.now()
        accepted = True
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                end_date=str(end_date),
                accepted=True
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_discount_accepted(self):
        discount = 0.0
        accepted = True
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                accepted=accepted
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        expected_json = "{u'items': [], u'accepted': True, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'discount': 0.0}" % (offer, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_offer(offer)

    def test_create_discount_accepted_comments(self):
        discount = 0.0
        accepted = True
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                accepted=accepted,
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        expected_json = "{u'_id': {u'$oid': u'%s'}, u'items': [], u'company': {u'$oid': u'%s'}, u'comments': u'Comentario', u'discount': 0.0, u'accepted': True}" % (offer, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_offer(offer)

    def test_create_discount_comments(self):
        discount = 0.0
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                discount=discount,
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        expected_json = "{u'_id': {u'$oid': u'%s'}, u'items': [], u'company': {u'$oid': u'%s'}, u'comments': u'Comentario', u'discount': 0.0, u'accepted': False}" % (offer, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_offer(offer)

    def test_create_start_date(self):
        start_date = datetime.datetime.now()
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                start_date=str(start_date)
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_start_date_end_date(self):
        start_date = datetime.datetime.now()
        end_date = datetime.datetime.now()
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                start_date=str(start_date),
                end_date=str(end_date)
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_start_date_accepted(self):
        start_date = datetime.datetime.now()
        accepted = True
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                start_date=str(start_date),
                accepted=accepted
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_start_date_comments(self):
        start_date = datetime.datetime.now()
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                start_date=str(start_date),
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_start_date_end_date_accepted(self):
        start_date = datetime.datetime.now()
        end_date = datetime.datetime.now()
        accepted = True
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                start_date=str(start_date),
                end_date=str(end_date),
                accepted=True
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_start_date_end_date_comments(self):
        start_date = datetime.datetime.now()
        end_date = datetime.datetime.now()
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                start_date=str(start_date),
                end_date=str(end_date),
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_start_date_end_date_accepted_comments(self):
        start_date = datetime.datetime.now()
        end_date = datetime.datetime.now()
        accepted = True
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                start_date=str(start_date),
                end_date=str(end_date),
                accepted=True,
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_start_date_accepted_comments(self):
        start_date = datetime.datetime.now()
        accepted = True
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                start_date=str(start_date),
                accepted=accepted,
                comments=comments

                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_end_date(self):
        end_date = datetime.datetime.now()
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                end_date=str(end_date)
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_end_date_accepted(self):
        end_date = datetime.datetime.now()
        accepted = True
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                end_date=str(end_date),
                accepted=True
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_end_date_comments(self):
        end_date = datetime.datetime.now()
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                end_date=str(end_date),
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)

    def test_create_end_date_accepted_comments(self):
        end_date = datetime.datetime.now()
        accepted = True
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                end_date=str(end_date),
                accepted=True
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        #is_date = isinstance(json_data["date"]["$date"], datetime.datetime)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(is_date, True)
        self.delete_dummy_offer(offer)
    
    def test_create_accepted(self):
        accepted = True
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                accepted=accepted
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        expected_json = "{u'items': [], u'accepted': True, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}}" % (offer, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_offer(offer)

    def test_create_accepted_comments(self):
        accepted = True
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                accepted=accepted,
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        expected_json = "{u'items': [], u'accepted': True, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'comments': u'Comentario'}" % (offer, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_offer(offer)

    def test_create_comments(self):
        comments = "Comentario"
        response = self.app.post('/offers',
            data=json.dumps(dict(
                auth_token=self.token,
                comments=comments
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        offer = str(json_d["_id"]["$oid"])
        expected_json = "{u'items': [], u'accepted': False, u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'comments': u'Comentario'}" % (offer, self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_offer(offer)

# #
# #    CUSTOMER
# #   -----------
# #
#     def create_dummy_customer(self):
#         # create dummy customer
#         business_name="Business corp."
#         response = self.app.post('/customers',
#             data=json.dumps(dict(
#                 auth_token=self.token,
#                 business_name=business_name,
#                 rfc=self.rfc
#                 )),
#             content_type='application/json')
#         json_data = json.loads(response.data)
#         json_d = json.loads(json_data["data"])
#         customer = str(json_d["_id"]["$oid"])
#         self.assertEqual(response.status_code, 200)
#         return customer

#     def delete_dummy_customer(self, customer):
#         response = self.app.delete('/customers/%s' % customer,
#             data=json.dumps(dict(
#                 auth_token=self.token
#                 )),
#             content_type='application/json')
#         self.assertEqual(response.status_code, 200)

#     def test_get_customers(self):
#         response = self.app.get('/customers?auth_token=%s' % self.token, content_type='application/json')
#         self.assertEqual(response.status_code, 200)

#     def test_customers(self):
#         business_name="Business corp."
#         rfc = "ROPL000003"
#         response = self.app.post('/customers',
#             data=json.dumps(dict(
#                 auth_token=self.token,
#                 business_name=business_name,
#                 rfc=self.rfc
#                 )),
#             content_type='application/json')
#         json_data = json.loads(response.data)
#         json_d = json.loads(json_data["data"])
#         customer = str(json_d["_id"]["$oid"])
#         expected_json = "{u'rfc': u'%s', u'business_name': u'Business corp.', u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'sales': []}" % (self.rfc, customer, self.owner)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(str(json_d), expected_json)
#         self.delete_dummy_customer(customer)

#     def test_customer_detail(self):
#         customer = self.create_dummy_customer()
#         response = self.app.get('/customers/%s?auth_token=%s' % (customer, self.token), content_type='application/json')
#         expected_json = "{u'rfc': u'%s', u'business_name': u'Business corp.', u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'sales': []}" % (self.rfc, customer, self.owner)
#         json_data = json.loads(response.data)
#         json_d = json.loads(json_data["data"])
#         self.assertEqual(str(json_d), expected_json)
#         self.assertEqual(response.status_code, 200)
#         self.delete_dummy_customer(customer)

#     def test_customer_update(self):
#         customer = self.create_dummy_customer()
#         business_name = "Business Update"
#         response = self.app.put('/customers/%s' % customer,
#             data=json.dumps(dict(
#                 auth_token=self.token,
#                 business_name=business_name
#                 )),
#             content_type='application/json')
#         expected_json = "{u'rfc': u'%s', u'business_name': u'Business Update', u'_id': {u'$oid': u'%s'}, u'company': {u'$oid': u'%s'}, u'sales': []}" % (self.rfc, customer, self.owner)
#         json_data = json.loads(response.data)
#         json_d = json.loads(json_data["data"])
#         self.assertEqual(str(json_d), expected_json)
#         self.assertEqual(response.status_code, 200)
#         self.delete_dummy_customer(customer)

#     def test_customer_delete(self):
#         customer = self.create_dummy_customer()
#         response = self.app.delete('/customers/%s' % customer,
#             data=json.dumps(dict(
#                 auth_token=self.token
#                 )),
#             content_type='application/json')
#         self.assertEqual(response.status_code, 200)


#     def test_customers_search(self):
#         response = self.app.get('/customers/search?auth_token=%s' % self.token, content_type='application/json')
#         self.assertEqual(response.status_code, 200)

#
#    SALE
#   -----------
#

    def create_dummy_sale(self):
        # create dummy sale
        response = self.app.post('/sales',
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        sale = str(json_d["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)
        return sale

    def delete_dummy_sale(self, sale):
        response = self.app.delete('/sales/%s' % sale,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)     
           
    def test_sales(self):
        response = self.app.post('/sales',
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        sale = str(json_d["_id"]["$oid"])
        expected_json = "{u'offers': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}}" % (self.owner, sale)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_sale(sale)

    def test_sale_detail(self):
        sale = self.create_dummy_sale()
        response = self.app.get('/sales/%s?auth_token=%s' % (sale, self.token), content_type='application/json')
        expected_json = "{u'offers': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}}" % (self.owner, sale)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_sale(sale)

    def test_sale_update(self):
        sale = self.create_dummy_sale()
        response = self.app.put('/sales/%s' % sale,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        expected_json = "{u'offers': [], u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}}" % (self.owner, sale)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_sale(sale)

    def test_sale_delete(self):
        sale = self.create_dummy_sale()
        response = self.app.delete('/sales/%s' % sale,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_sales_search(self):
        response = self.app.get('/sales/search?auth_token=%s' % self.token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    COMPANY
#   -----------
#

    def create_dummy_company(self):
        # create dummy company
        name = "Hola Inc."
        direction = "Direccion hol aloha"
        response = self.app.post('/companies',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                direction=direction
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        company = str(json_d["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)
        return company

    def delete_dummy_company(self, company):
        response = self.app.delete('/companies/%s' % company,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # def test_get_companies(self):
    #     response = self.app.get('/companies?auth_token=%s' % self.token, content_type='application/json')
    #     self.assertEqual(response.status_code, 200)

    def test_companies(self):
        name = "Hola Inc."
        direction = "Direccion hol aloha"
        response = self.app.post('/companies',
            data=json.dumps(dict(
                auth_token=self.token,
                name=name,
                direction=direction
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        company = str(json_d["_id"]["$oid"])
        expected_json = "{u'direction': u'%s', u'_id': {u'$oid': u'%s'}, u'name': u'%s'}" % (direction, company, name)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_company(company)

    def test_company_detail(self):
        company = self.create_dummy_company()
        name = "Hola Inc."
        direction = "Direccion hol aloha"
        response = self.app.get('/companies/%s?auth_token=%s' % (company, self.token), content_type='application/json')
        expected_json = "{u'direction': u'%s', u'_id': {u'$oid': u'%s'}, u'name': u'%s'}" % (direction, company, name)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_company(company)

    def test_company_update(self):
        company = self.create_dummy_company()
        name = "Hola Update"
        direction = "Direccion hol aloha"
        response = self.app.put('/companies/%s' % company,
            data=json.dumps(dict(
                auth_token=self.token,
                name=name
                )),
            content_type='application/json')
        expected_json = "{u'direction': u'%s', u'_id': {u'$oid': u'%s'}, u'name': u'%s'}" % (direction, company, name)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_company(company)

    def test_company_delete(self):
        company = self.create_dummy_company()
        response = self.app.delete('/companies/%s' % company,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_companys_search(self):
        response = self.app.get('/companies/search?auth_token=%s' % self.token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

#
#    TEAM
#   -----------
#

    def create_dummy_team(self):
        # create dummy team
        response = self.app.post('/teams',
            data=json.dumps(dict(
                auth_token=self.token,
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        team = str(json_d["_id"]["$oid"])
        self.assertEqual(response.status_code, 200)
        return team

    def delete_dummy_team(self, team):
        response = self.app.delete('/teams/%s' % team,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_teams(self):
        response = self.app.get('/teams?auth_token=%s' % self.token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_teams(self):
        response = self.app.post('/teams',
            data=json.dumps(dict(
                auth_token=self.token,
                )),
            content_type='application/json')
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        team = str(json_d["_id"]["$oid"])
        expected_json = "{u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'sales': [], u'members': []}" % (self.owner, team)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(json_d), expected_json)
        self.delete_dummy_team(team)

    def test_team_detail(self):
        team = self.create_dummy_team()
        response = self.app.get('/teams/%s?auth_token=%s' % (team, self.token), content_type='application/json')
        expected_json = "{u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'sales': [], u'members': []}" % (self.owner, team)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_team(team)

    def test_team_update(self):
        team = self.create_dummy_team()
        business_name = "Business Update"
        response = self.app.put('/teams/%s' % team,
            data=json.dumps(dict(
                auth_token=self.token,
                business_name=business_name
                )),
            content_type='application/json')
        expected_json = "{u'company': {u'$oid': u'%s'}, u'_id': {u'$oid': u'%s'}, u'sales': [], u'members': []}" % (self.owner, team)
        json_data = json.loads(response.data)
        json_d = json.loads(json_data["data"])
        self.assertEqual(str(json_d), expected_json)
        self.assertEqual(response.status_code, 200)
        self.delete_dummy_team(team)

    def team_delete(self):
        team = self.create_dummy_team()
        response = self.app.delete('/teams/%s' % team,
            data=json.dumps(dict(
                auth_token=self.token
                )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_teams_search(self):
        response = self.app.get('/teams/search?auth_token=%s' % self.token, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()