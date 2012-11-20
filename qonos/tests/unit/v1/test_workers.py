import uuid
import webob.exc

from qonos.api.v1 import workers
from qonos.common import exception
import qonos.db.simple.api as db_api
from qonos.tests import utils as test_utils
from qonos.tests.unit import utils as unit_test_utils
from qonos.tests.unit.utils import WORKER_UUID1


class TestWorkersApi(test_utils.BaseTestCase):

    def setUp(self):
        super(TestWorkersApi, self).setUp()
        self.controller = workers.WorkersController()

    def test_list(self):
        request = unit_test_utils.get_fake_request(method='GET')
        worker = db_api.worker_create({'host': 'ameade.cow'})
        workers = self.controller.list(request).get('workers')
        self.assertTrue(worker in workers)

    def test_get(self):
        request = unit_test_utils.get_fake_request(method='GET')
        expected = db_api.worker_create({'host': 'ameade.cow'})
        actual = self.controller.get(request, expected['id']).get('worker')
        self.assertEqual(actual, expected)

    def test_get_not_found(self):
        request = unit_test_utils.get_fake_request(method='GET')
        worker_id = str(uuid.uuid4())
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.controller.get, request, worker_id)

    def test_create(self):
        request = unit_test_utils.get_fake_request(method='POST')
        host = 'ameade.cow'
        fixture = {'worker': {'host': host}}
        actual = self.controller.create(request, fixture)['worker']
        self.assertEqual(host, actual['host'])

    def test_delete(self):
        request = unit_test_utils.get_fake_request(method='GET')
        worker = db_api.worker_create({'host': 'ameade.cow'})
        request = unit_test_utils.get_fake_request(method='DELETE')
        self.controller.delete(request, worker['id'])
        self.assertRaises(exception.NotFound, db_api.worker_get_by_id,
                          worker['id'])

    def test_delete_not_found(self):
        request = unit_test_utils.get_fake_request(method='DELETE')
        worker_id = str(uuid.uuid4())
        self.assertRaises(webob.exc.HTTPNotFound,
                          self.controller.delete, request, worker_id)

    def test_get_next_job_unimplemented(self):
        request = unit_test_utils.get_fake_request(method='PUT')
        self.assertRaises(webob.exc.HTTPNotImplemented,
                          self.controller.get_next_job, request,
                          WORKER_UUID1)