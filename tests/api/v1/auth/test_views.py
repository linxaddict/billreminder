import json

import tests.api.v1.auth.fixtures as f
from billreminder.api.v1.profile.models import User
from billreminder.http_status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_200_OK, \
    HTTP_401_UNAUTHORIZED
from tests.base import BaseTest

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class RegistrationViewTest(BaseTest):
    url = '/api/v1/auth/register'

    def test_register(self):
        data = f.user_dict()
        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        user = User.get_by_email(data['email'])

        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])

    def test_register_no_input_data(self):
        data = {}
        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_register_user_already_exists(self):
        data = f.user_dict()
        f.user(**data)

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_409_CONFLICT)

    def test_register_invalid_email(self):
        data = f.user_dict()
        data['email'] = 'invalid_email'

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_register_password_too_short(self):
        data = f.user_dict()
        data['password'] = 'abcd'

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_register_missing_email(self):
        data = f.user_dict()
        del data['email']

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_register_missing_password(self):
        data = f.user_dict()
        del data['password']

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


class LoginViewTest(BaseTest):
    url = '/api/v1/auth/login'

    def test_login(self):
        f.user()
        data = f.login_dict()

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue('token' in response.json)
        self.assertTrue(response.json['token'])

    def test_login_no_input_data(self):
        data = {}
        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_login_unknown_email(self):
        f.user()
        data = f.login_dict(email='test@test.com')

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_login_unknown_bad_password(self):
        f.user()
        data = f.login_dict(password='bad_password')

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_login_user_doesnt_exist(self):
        data = f.login_dict()
        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
