
from tests.base import BaseTestCase 
from app.models import User
from app import db
import unittest
import json

class TestBledataBluePrint(BaseTestCase):
###
### UPLOAD DATA TEST
###
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
    
    def test_bledata_upload_with_missed_mac(self):
        """
        Test upload bledata with missed mac
        :return:
        """
        with self.client:
            response = self.upload_data(level=-50, time='2020-11-10T16:17:25')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Wrong mac format')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)
    
    def test_bledata_upload_with_missed_level(self):
        """
        Test upload bledata with missed level
        :return:
        """
        with self.client:
            response = self.upload_data(mac='11-22-33-44-55-65', time='2020-11-10T16:17:25')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Wrong data format')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)

    def test_bledata_upload_with_missed_time(self):
        """
        Test upload bledata with missed time
        :return:
        """
        with self.client:
            response = self.upload_data(mac='11-22-33-44-55-65', level=-50)
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Wrong time format')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)

    def test_bledata_upload_with_no_params(self):
        """
        Test upload bledata with no parameters
        :return:
        """
        with self.client:
            response = self.upload_data()
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Wrong data format')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)
###
### END UPLOAD DATA TEST
###


###
### DELETE DATA TEST
###
    def test_bledata_delete_all_data(self):
        """
        Test upload a few data and delete all
        :return:
        """
        token = self.get_user_token()

        if self.upload_dummy_data():
            with self.client:
                response = self.client.delete(
                        '/api/bledata/delete',
                        content_type='application/json',
                        headers={'x-access-token':token})
                data = json.loads(response.data.decode())
                self.assertTrue(data['deleted'] == 3)
                self.assertTrue(data['error'] is None)
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 200)
    
    def test_bledata_delete_no_data(self):
        """
        Test delete when no data
        :return:
        """
        token = self.get_user_token()

        with self.client:
            response = self.client.delete(
                    '/api/bledata/delete',
                    content_type='application/json',
                    headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Nothing deleted')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)
###
### END DELETE DATA TEST
###


###
### GET DATA TEST
###
    def test_bledata_get_all_data(self):
        """
        Test get all data
        :return:
        """
        token = self.get_user_token()

        if self.upload_dummy_data():
            with self.client:
                response = self.client.get(
                        '/api/bledata/',
                        content_type='application/json',
                        headers={'x-access-token':token})
                data = json.loads(response.data.decode())
                self.assertTrue(data['error'] is None)
                self.assertTrue(data['totalCount'] == 3)
                for dat in data['items']:
                    self.assertTrue(dat['level'] is not None)
                    self.assertTrue(dat['mac'] is not None)
                    self.assertTrue(dat['time'] is not None)
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 200)
    
    def test_bledata_get_all_when_no_data(self):
        """
        Test get all data when database empty
        :return:
        """
        token = self.get_user_token()

        with self.client:
            response = self.client.get(
                    '/api/bledata/',
                    content_type='application/json',
                    headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] is None)
            self.assertTrue(data['totalCount'] == 0)
            self.assertTrue(len(data['items']) == 0)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
    
    def test_bledata_get_data_by_mac(self):
        """
        Test get all data by mac
        :return:
        """
        token = self.get_user_token()

        if self.upload_dummy_data():
            with self.client:
                response = self.client.post(
                        '/api/bledata/',
                        content_type='application/json',
                        json={'mac':'11-22-33-44-55-66'},
                        headers={'x-access-token':token})
                data = json.loads(response.data.decode())
                self.assertTrue(data['error'] is None)
                self.assertTrue(data['totalCount'] == 1)
                for dat in data['items']:
                    self.assertTrue(dat['level'] is not None)
                    self.assertTrue(dat['time'] is not None)
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 200)

    def test_bledata_get_data_by_wrong_mac(self):
        """
        Test get all data by wrong mac
        :return:
        """
        token = self.get_user_token()

        if self.upload_dummy_data():
            with self.client:
                response = self.client.post(
                        '/api/bledata/',
                        content_type='application/json',
                        json={'mac':'11'},
                        headers={'x-access-token':token})
                data = json.loads(response.data.decode())
                self.assertTrue(data['error'] == 'Wrong mac format')
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 403) 
  
    def test_bledata_get_data_by_missed_mac(self):
        """
        Test get all data by missed mac
        :return:
        """
        token = self.get_user_token()

        if self.upload_dummy_data():
            with self.client:
                response = self.client.post(
                        '/api/bledata/',
                        content_type='application/json',
                        headers={'x-access-token':token})
                data = json.loads(response.data.decode())
                self.assertTrue(data['error'] == 'Missing header')
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 401)  

    def test_bledata_get_data_with_pagin(self):
        """
        Test get data with pagination by correct count and page
        :return:
        """
        token = self.get_user_token()

        if self.upload_dummy_data():
            with self.client:
                response = self.client.get(
                        '/api/bledata/?count=1&page=2',
                        content_type='application/json',
                        headers={'x-access-token':token})
                data = json.loads(response.data.decode())
                self.assertTrue(data['error'] is None)
                self.assertTrue(data['totalCount'] == 3)
                for dat in data['items']:
                    self.assertTrue(dat['level'] is not None)
                    self.assertTrue(dat['mac'] is not None)
                    self.assertTrue(dat['time'] is not None)
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 200)   

    def test_bledata_get_data_with_pagin_abnormal_count(self):
        """
        Test get data with pagination by not normal count
        :return:
        """
        token = self.get_user_token()

        if self.upload_dummy_data():
            with self.client:
                response = self.client.get(
                        '/api/bledata/?count=1000&page=2',
                        content_type='application/json',
                        headers={'x-access-token':token})
                data = json.loads(response.data.decode())
                self.assertTrue(data['error'] == "Wrong page or count")
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 403)  

    def test_bledata_get_data_with_pagin_abnormal_page(self):
        """
        Test get data with pagination by not normal page
        :return:
        """
        token = self.get_user_token()

        if self.upload_dummy_data():
            with self.client:
                response = self.client.get(
                        '/api/bledata/?count=1&page=2000',
                        content_type='application/json',
                        headers={'x-access-token':token})
                data = json.loads(response.data.decode())
                self.assertTrue(data['error'] == "Wrong page or count")
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 403)                
###
### END GET DATA TEST
###
