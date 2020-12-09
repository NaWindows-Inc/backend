from tests.base import BaseTestCase 
from app import db
import unittest
import json

class TestErrorBluePrint(BaseTestCase):
    def test_404_page_error(self):
        """
        Test unknown page get
        :return:
        """
        with self.client:
            response = self.client.get(
                    '/wrong_page',
                    content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == "Not found page")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404) 
    
    def test_405_page_error(self):
        """
        Test not allowed method for the requested URLs
        :return:
        """
        with self.client:
            response = self.client.get(
                    '/user/update',
                    content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == "The method is not allowed for the requested URL")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 405) 
    
    def test_check_token_life(self):
        """
        Test check token life page
        :return:
        """
        token = self.get_user_token()

        with self.client:
            response = self.client.get(
                    '/hello',
                    content_type='application/json',
                    headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['remaining'] > 0)
            self.assertTrue(data['valid'] == True) 
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200) 
    
    def test_check_token_life_with_invalid_token(self):
        """
        Test check token life page
        :return:
        """
        token = self.get_user_token()
        token += "wrong_part"

        with self.client:
            response = self.client.get(
                    '/hello',
                    content_type='application/json',
                    headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Invalid token')
            self.assertTrue(data['remaining'] is None)
            self.assertTrue(data['valid'] == False)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 402) 