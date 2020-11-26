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
            # content_type='application/json',
            data={'username':username, 'email':email, 'password':password})

    def login_user(self, email='', password=''):
        """
        Helper method for login a user with dummy data
        :return:
        """
        return self.client.post(
            '/user/login',
            data={'email':email, 'password':password})

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