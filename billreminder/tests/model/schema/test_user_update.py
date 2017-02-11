from unittest import TestCase

from billreminder.model.schemas import UserUpdateSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestUserUpdateSchema(TestCase):
    def test_load(self):
        data = {
            'email': 'test@gmail.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name'
        }

        schema = UserUpdateSchema()
        loaded, errors = schema.load(data)

        self.assertEqual(len(errors.keys()), 0)

        self.assertEqual(data['email'], loaded['email'])
        self.assertEqual(data['first_name'], loaded['first_name'])
        self.assertEqual(data['last_name'], loaded['last_name'])

    def test_load_invalid_email(self):
        data = {
            'email': 'test_gmail.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name'
        }

        schema = UserUpdateSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('email' in errors)

        self.assertEqual(data['first_name'], loaded['first_name'])
        self.assertEqual(data['last_name'], loaded['last_name'])

    def test_dump(self):
        data = {
            'email': 'test@gmail.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name'
        }

        schema = UserUpdateSchema()
        dumped = schema.dump(data).data

        self.assertEqual(data['email'], dumped['email'])
        self.assertEqual(data['first_name'], dumped['first_name'])
        self.assertEqual(data['last_name'], dumped['last_name'])
