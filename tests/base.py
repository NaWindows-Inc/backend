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
        app.config.from_object('app.config.Development')
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

    def register_user(self, username, email, password):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        return self.client.post(
            'user/signup',
            content_type='application/json;charset=utf-8',
            data=json.dumps(dict(username=username, email=email, password=password)))

    def get_user_token(self):
        """
        Get a user token
        :return:
        """
        auth_res = self.register_user('test', 'test@test.com', 'test123')
        return json.loads(jwt.decode(auth_res, app.config['SECRET_KEY']) )['auth_token']