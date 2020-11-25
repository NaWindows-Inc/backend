from flask_testing import TestCase
from app import app
from flask import current_app
import unittest
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        """
        Create an app with the development configuration
        :return:
        """
        app.config.from_object('app.config.Development')
        return app

    def test_app_in_development(self):
        """
        Test that the development configs are set correctly.
        :return:
        """
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == getenv("DATABASE_URL"))
        self.assertTrue(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False)
        self.assertFalse(app.config['SECRET_KEY'] == 'secret_key')
        self.assertTrue(app.config['JWT_BLACKLIST_ENABLED'], True)
        self.assertEqual(app.config['FLASK_APP'], 'run.py')
        self.assertTrue(app.config['DEBUG'], True)
        self.assertTrue(app.config['TESTING'], True)
        self.assertEqual(app.config['ENV'], 'development')
        self.assertFalse(current_app is None)
        

class TestProductionConfig(TestCase):
    def create_app(self):
        """
        Create an app with the production configuration
        :return:
        """
        app.config.from_object('app.config.Production')
        return app
    
    def test_app_in_production(self):
        """
        Test that the production configs are set correctly.
        :return:
        """
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == getenv("DATABASE_URL"))
        self.assertTrue(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False)
        self.assertFalse(app.config['SECRET_KEY'] == 'secret_key')
        self.assertTrue(app.config['JWT_BLACKLIST_ENABLED'], True)
        self.assertEqual(app.config['FLASK_APP'], 'run.py')
        self.assertTrue(app.config['DEBUG'] == False)
        self.assertTrue(app.config['TESTING'] ==  False)
        self.assertEqual(app.config['ENV'], 'production')
        self.assertFalse(current_app is None)


if __name__ == '__main__':
    unittest.main()