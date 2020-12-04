
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
            self.assertTrue(data['error'] == None)
            self.assertTrue(data['response'] == "Successfully registered")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_with_missing_username(self):
        """
        Test a user registration with missing username 
        :return:
        """
        with self.client:
            response = self.register_user(email='test@test.com', password='test123')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == "Missing username or email or password")
            self.assertTrue(data['response'] == None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)

    def test_user_registration_with_missing_email(self):
        """
        Test a user registration with missing email 
        :return:
        """
        with self.client:
            response = self.register_user(username='test', password='test123')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == "Missing username or email or password")
            self.assertTrue(data['response'] == None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)
    
    def test_user_registration_with_missing_password(self):
        """
        Test a user registration with missing password 
        :return:
        """
        with self.client:
            response = self.register_user(email='test@test.com', username='test')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == "Missing username or email or password")
            self.assertTrue(data['response'] == None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)
    
    def test_user_registration_with_missing_two_parameters(self):
        """
        Test a user registration with missing two parameters 
        :return:
        """
        with self.client:
            response = self.register_user(email='test@test.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == "Missing username or email or password")
            self.assertTrue(data['response'] == None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)
    
    def test_user_registration_with_the_same_email(self):
        """
        Test a user registration with the same email as different user
        :return:
        """
        self.register_user(username='test1', email='test@test.com', password='test123')

        with self.client:
            response = self.register_user('test2', 'test@test.com', 'test123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == "User already exists. Please Log in")
            self.assertTrue(data['response'] == None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)
    
    def test_user_login_with_valid_data(self):
        """
        Test a user login with valid email and password
        :return:
        """
        self.register_user(username='test', email='test@test.com', password='test123')

        with self.client:
            response = self.login_user('test@test.com', 'test123')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] is None)
            data = data['response']
            self.assertFalse(data['token'] is None)
            self.assertTrue(data['username'] == 'test')
            self.assertFalse(data['id'] is None)
            self.assertTrue(data['email'] == 'test@test.com')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
    
    def test_user_login_with_invalid_email(self):
        """
        Test a user login with invalid email
        :return:
        """
        self.register_user(username='test', email='test@test.com', password='test123')

        with self.client:
            response = self.login_user('wrongemail@test.com', 'test123')
            data = json.loads(response.data.decode())
            self.assertTrue(data['response'] is None)
            self.assertTrue(data['error'] == 'User does not exist')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_user_login_with_invalid_password(self):
        """
        Test a user login with invalid password
        :return:
        """
        self.register_user(username='test', email='test@test.com', password='test123')

        with self.client:
            response = self.login_user('test@test.com', 'wrondpassword')
            data = json.loads(response.data.decode())
            self.assertTrue(data['response'] is None)
            self.assertTrue(data['error'] == 'Wrong password')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)

    def test_user_login_with_missed_password(self):
        """
        Test a user login with missed password
        :return:
        """
        self.register_user(username='test', email='test@test.com', password='test123')

        with self.client:
            response = self.login_user(email='test@test.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['response'] is None)
            self.assertTrue(data['error'] == 'Missing email or password')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)
    
    def test_user_login_with_missed_email(self):
        """
        Test a user login with missed email
        :return:
        """
        self.register_user(username='test', email='test@test.com', password='test123')

        with self.client:
            response = self.login_user(password='wrondpassword')
            data = json.loads(response.data.decode())
            self.assertTrue(data['response'] is None)
            self.assertTrue(data['error'] == 'Missing email or password')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)
    
    def test_user_logout(self):
        """
        Test a user logout
        :return:
        """
        token = self.get_user_token()

        with self.client:
            response = self.client.delete(
                '/user/logout',
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['response'] == 'Successfully logged out')
            self.assertTrue(data['error'] is None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
    
    def test_user_operation_without_token(self):
        """
        Test a user operation without token
        :return:
        """
        token = self.get_user_token()

        with self.client:
            response = self.client.delete(
                '/user/logout')
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Login required')
            self.assertTrue(data['remaining'] is None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)
    
    def test_user_operation_with_wrong_token(self):
        """
        Test a user operation with wrong token
        :return:
        """
        token = self.get_user_token()

        with self.client:
            response = self.client.delete(
                '/user/logout',
                headers={'x-access-token':token+"wrong_part"})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Invalid token')
            self.assertTrue(data['remaining'] is None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 402)
    
    def test_get_all_users(self):
        """
        Test getting all users
        :return:
        """
        self.register_user(username='test2', email='test2@test.com', password='test123')
        token = self.get_user_token()

        with self.client:
            response = self.client.get(
                '/user/',
                headers={'x-access-token':token})
            datas = json.loads(response.data.decode())
            self.assertTrue(datas['error'] is None)
            for data in datas['users']:
                self.assertFalse(data['email'] is None)
                self.assertFalse(data['id'] is None)
                self.assertFalse(data['public_id'] is None)
                self.assertFalse(data['username'] is None)
                self.assertTrue(response.content_type == 'application/json')
                self.assertEqual(response.status_code, 200)
    
    def test_get_user_by_id(self):
        """
        Test getting user by id 
        :return:
        """
        self.register_user(username='test', email='test@test.com', password='test123')
        response = self.login_user(email='test@test.com', password='test123')
        data = json.loads(response.data.decode())
        data = data['response']
        token = data['token']
        url = '/user/'+'?id='+str(data['id'])

        with self.client:
            response = self.client.get(
                url,
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] is None)
            self.assertFalse(data['email'] is None)
            self.assertFalse(data['id'] is None)
            self.assertFalse(data['public_id'] is None)
            self.assertFalse(data['username'] is None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_get_user_by_wrong_id(self):
        """
        Test getting user by wrong id 
        :return:
        """
        self.register_user(username='test', email='test@test.com', password='test123')
        response = self.login_user(email='test@test.com', password='test123')
        data = json.loads(response.data.decode())
        data = data['response']
        token = data['token']
        url = '/user/'+'?id=111'+str(data['id'])

        with self.client:
            response = self.client.get(
                url,
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Wrong id')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)

    def test_user_update_password(self):
        """
        Test update password of user
        :return:
        """
        token = self.get_user_token()
        
        with self.client:
            response = self.client.put(
                "/user/update",
                data={'password':'new_password'},
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] is None)
            self.assertTrue(data['response'] == 'Succesfully updated')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_user_update_username(self):
        """
        Test update username of user
        :return:
        """
        token = self.get_user_token()
        
        with self.client:
            response = self.client.put(
                "/user/update",
                data={'username':'new_username'},
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] is None)
            self.assertTrue(data['response'] == 'Succesfully updated')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
    
    def test_user_update_email(self):
        """
        Test update email of user
        :return:
        """
        token = self.get_user_token()
        
        with self.client:
            response = self.client.put(
                "/user/update",
                data={'email':'new_email@gmail.com'},
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] is None)
            self.assertTrue(data['response'] == 'Succesfully updated')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_user_update_email_and_password(self):
        """
        Test update email and password of user
        :return:
        """
        token = self.get_user_token()
        
        with self.client:
            response = self.client.put(
                "/user/update",
                data={'email':'new_email@gmail.com', "password":'new_password'},
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] is None)
            self.assertTrue(data['response'] == 'Succesfully updated')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_user_update_with_wrong_parameter(self):
        """
        Test update with wrong parameter of user
        :return:
        """
        token = self.get_user_token()
        
        with self.client:
            response = self.client.put(
                "/user/update",
                data={'something':'new_email@gmail.com'},
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['response'] is None)
            self.assertTrue(data['error'] == 'Something went wrong')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)

    def test_user_update_with_missed_parameter(self):
        """
        Test update with missed parameter of user
        :return:
        """
        token = self.get_user_token()
        
        with self.client:
            response = self.client.put(
                "/user/update",
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['response'] is None)
            self.assertTrue(data['error'] == 'Not data for update')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_user_delete_by_id(self):
        """
        Test delete the user by id
        :return:
        """
        self.register_user(username='test', email='test@test.com', password='test123')
        response = self.login_user(email='test@test.com', password='test123')
        data = json.loads(response.data.decode())
        data = data['response']
        url = '/user/delete'+'?id='+str(data['id'])
        token = self.get_user_token()

        with self.client:
            response = self.client.delete(
                url,
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['response'] == 'Succesfully deleted user')
            self.assertTrue(data['error'] is None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_user_delete_with_missed_id(self):
        """
        Test delete the user with missed id
        :return:
        """
        token = self.get_user_token()
        self.register_user(username='test', email='test@test.com', password='test123')

        with self.client:
            response = self.client.delete(
                '/user/delete',
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Wrong user id')
            self.assertTrue(data['response'] is None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_user_delete_with_wrong_id(self):
        """
        Test delete the user with wrong id
        :return:
        """
        token = self.get_user_token()
        self.register_user(username='test', email='test@test.com', password='test123')

        with self.client:
            response = self.client.delete(
                '/user/delete?id=1000',
                headers={'x-access-token':token})
            data = json.loads(response.data.decode())
            self.assertTrue(data['error'] == 'Something went wrong')
            self.assertTrue(data['response'] is None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)