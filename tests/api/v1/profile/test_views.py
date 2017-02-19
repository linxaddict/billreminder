import json

from billreminder.api.v1.profile.schemas import UserSchema
from billreminder.http_status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from tests.base import ViewTestMixin, BaseTest
import tests.api.v1.profile.fixtures as f

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class UserViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/profile'

    def test_fetch(self):
        self.current_user.avatar = 'test_avatar'

        response = self.client.get(self.url, content_type=self.json_content_type, headers=self.auth_header)
        schema = UserSchema()

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(schema.dump(self.current_user).data, response.json)

    def test_fetch_unauthorized(self):
        self.token = None
        response = self.client.get(self.url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)

    def test_update(self):
        update_data = f.user_dict(email='a@b.com', password='p1234', first_name='f', last_name='l')
        response = self.client.put(self.url, data=json.dumps(update_data), content_type=self.json_content_type,
                                   headers=self.auth_header)
        schema = UserSchema()

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(schema.dump(self.current_user).data, response.json)

        self.assertEqual(self.current_user.first_name, update_data['first_name'])
        self.assertEqual(self.current_user.last_name, update_data['last_name'])

    def test_update_email_not_changed(self):
        update_data = f.user_dict(email='a@b.com', password='p1234', first_name='f', last_name='l')
        response = self.client.put(self.url, data=json.dumps(update_data), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_200_OK)
        self.assertNotEqual(self.current_user.email, update_data['email'])

    def test_update_avatar_not_changed(self):
        update_data = f.user_dict(email='a@b.com', password='p1234', first_name='f', last_name='l')
        update_data['avatar'] = 'abcd'
        response = self.client.put(self.url, data=json.dumps(update_data), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_200_OK)
        self.assertNotEqual(self.current_user.avatar, update_data['avatar'])

    def test_update_no_input_data(self):
        response = self.client.put(self.url, data=json.dumps({}), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_update_unauthorized(self):
        self.token = None
        response = self.client.put(self.url, data=json.dumps({}), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)
