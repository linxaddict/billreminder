import json

from flask_testing import TestCase

from billreminder.api.v1.auth.models import User
from billreminder.extensions import db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class BaseTest(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.db = db

    def create_app(self):
        from autoapp import app
        return app

    @property
    def json_content_type(self):
        return 'application/json'

    def setUp(self):
        super().setUp()
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.db.get_engine(self.app).dispose()


class ViewTestMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None

    def setUp(self):
        super().setUp()

        self.register()
        self.login()

    def register(self, email='test@email.com', password='password1234'):
        url = '/api/v1/auth/register'
        auth_data = {
            'email': email,
            'password': password
        }

        self.client.post(url, data=json.dumps(auth_data), content_type=self.json_content_type)

    def login(self, email='test@email.com', password='password1234'):
        url = '/api/v1/auth/login'
        auth_data = {
            'email': email,
            'password': password
        }

        response = self.client.post(url, data=json.dumps(auth_data), content_type=self.json_content_type)
        self.token = response.json['token']

    @property
    def auth_header(self):
        return {
            'Auth-Token': self.token
        }

    @property
    def current_user(self):
        return User.verify_auth_token(self.token)
