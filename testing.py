import unittest
import os
import tempfile
from app import app
from base64 import b64encode



class TestTodo(unittest.TestCase):
    """unittest for application and Api"""

    def setUp(self):
        """create testing client"""

        self.database, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()

    def teardown(self):
        os.close(self.database)
        os.unlink(app.config['DATABASE'])

    def test_index(self):
        """test that index template returns 200 status code"""

        request = self.app.get('/')
        self.assertEqual(request.status_code, 200)

    def test_todo_list_api(self):
        """test that get api resource for todo list returns 200 status code"""

        request = self.app.get('/api/v1/todos')
        self.assertEqual(request.status_code, 200)

    def test_post_todo_list(self):
        """test that post api resource for todo list returns 200 status code"""

        request = self.app.post('/api/v1/todos')
        self.assertEqual(request.status_code, 200)

    def test_todo_item(self):
        """test that api resource for specific task returns 404 status code if no task has
           been created
        """

        request = self.app.get('/api/v1/todos/1')
        self.assertEqual(request.status_code, 404) #getting 404 on item

    def test_user(self):
        """test that api resource for user returns 405 status code"""

        request = self.app.get('/api/v1/users')
        self.assertEqual(request.status_code, 405)#getting 405




if __name__ == '__main__':
    unittest.main()
