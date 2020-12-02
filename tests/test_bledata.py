
from tests.base import BaseTestCase 
from app.models import User
from app import db
import unittest
import json

class TestBledataBluePrint(BaseTestCase):
    def test_bledata_upload_with_right_format(self):
        """
        Test upload bledata with right format
        :return:
        """
        with self.client:
            response = self.upload_data(mac='11-22-33-44-55-66', level=-50, time='2020-11-10T16:17:25')
            data = json.loads(response.data.decode())
            self.assertTrue(data['level'] == -50)
            self.assertTrue(data['mac'] == '11-22-33-44-55-66')
            self.assertTrue(data['time'] == '2020-11-10T16:17:25')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_bledata_upload_with_wrong_mac(self):
        """
        Test upload bledata with wrong mac
        :return:
        """
        with self.client:
            response = self.upload_data(mac='11-22-33-44-55-6', level=-50, time='2020-11-10T16:17:25')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Wrong mac format')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)

    def test_bledata_upload_with_wrong_level(self):
        """
        Test upload bledata with wrong level
        :return:
        """
        with self.client:
            response = self.upload_data(mac='11-22-33-44-55-65', level="wrong_level", time='2020-11-10T16:17:25')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Wrong data format')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)

    def test_bledata_upload_with_wrong_time(self):
        """
        Test upload bledata with wrong time
        :return:
        """
        with self.client:
            response = self.upload_data(mac='11-22-33-44-55-65', level=-50, time='wrong_time')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Wrong time format')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)

#TODO test for error 404, 405, 500, delete, check_token, bledata views