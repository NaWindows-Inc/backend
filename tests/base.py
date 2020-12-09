from app import app, db
from flask_testing import TestCase
import json
import jwt #for PyJWT authentication 


class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        :return:
        """
        app.config.from_object('app.config.Testing')
        return app
    
    def setUp(self):
        """
        Create the database
        :return:
        """
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """
        Drop the database tables and also remove the session
        :return:
        """
        db.session.remove()
        db.drop_all()

    def register_user(self, username='', email='', password=''):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        return self.client.post(
            '/user/signup',
            content_type='application/json',
            json={'username':username, 'email':email, 'password':password})

    def login_user(self, email='', password=''):
        """
        Helper method for login a user with dummy data
        :return:
        """
        return self.client.post(
            '/user/login',
            content_type='application/json',
            json={'email':email, 'password':password})

    def get_user_token(self):
        """
        Get a user token
        :return:
        """
        self.register_user(username='test', email='test@test.com', password='test123')
        response = self.login_user(email='test@test.com', password='test123')
        data = json.loads(response.data.decode())
        data = data['response']
        return data['token']
    
    def upload_data(self, mac='', level='', time=''):
        """
        Upload data
        :return:
        """
        return self.client.post(
            '/api/bledata/upload',
            content_type='application/json',
            json={'mac':mac, 'level':level, 'time': time})
    
    def upload_dummy_data(self):
        """
        Upload a few dummy data
        :return:
        """
        self.upload_data(mac='11-22-33-44-55-66', level=-50, time='2020-11-10T16:17:25')
        self.upload_data(mac='11-22-33-44-55-77', level=-60, time='2020-11-10T16:18:25')
        self.upload_data(mac='11-22-33-44-55-88', level=-70, time='2020-11-10T16:19:25')
        return True