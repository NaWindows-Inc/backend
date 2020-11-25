
from tests.base import BaseTestCase 
from app.models import User
from app import db
import unittest
import json

class TestUserBluePrint(BaseTestCase):
    def test_user_registration(self):
        """
        Test a user is successfully created through the api
        :return:
        """
        with self.client:
            response = self.register_user('test', 'test@test.com', 'test123')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'null')
            self.assertTrue(data['response'] == "Successfully registered")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)