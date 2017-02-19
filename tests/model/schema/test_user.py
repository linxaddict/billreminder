from unittest import TestCase

from billreminder.api.v1.profile.schemas import UserSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestUserSchema(TestCase):
    def test_load(self):
        data = {
            'id': 1,
            'email': 'email@test.com',
            'password': 'abcd1234',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = UserSchema()
        user = schema.load(data).data

        self.assertEqual(user['id'], data['id'])
        self.assertEqual(user['email'], data['email'])
        self.assertEqual(user['password'], data['password'])
        self.assertEqual(user['first_name'], data['first_name'])
        self.assertEqual(user['last_name'], data['last_name'])
        self.assertEqual(user['avatar'], data['avatar'])

    def test_load_invalid_email(self):
        data = {
            'id': 1,
            'email': 'email_test.com',
            'password': 'abcd1234',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = UserSchema()
        user, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('email' in errors)

    def test_load_empty_email(self):
        data = {
            'id': 1,
            'email': '',
            'password': 'abcd1234',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = UserSchema()
        user, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('email' in errors)

    def test_load_email_is_none(self):
        data = {
            'id': 1,
            'email': None,
            'password': 'abcd1234',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = UserSchema()
        user, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('email' in errors)

    def test_load_invalid_password(self):
        data = {
            'email': 'email@test.com',
            'password': 'abcd1'
        }

        schema = UserSchema()
        user, errors = schema.load(data)

        self.assertTrue('password' in errors)

    def test_load_password_is_none(self):
        data = {
            'email': 'email@test.com',
            'password': None
        }

        schema = UserSchema()
        user, errors = schema.load(data)

        self.assertTrue('password' in errors)

    def test_load_only_required_fields_needed(self):
        data = {
            'email': 'email@test.com',
            'password': 'abcd1234'
        }

        schema = UserSchema()
        user, errors = schema.load(data)

        self.assertFalse(errors)

    def test_load_required_fields_missing(self):
        data = {
            'id': 1,
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = UserSchema()
        user, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('email' in errors)
        self.assertTrue('password' in errors)

    def test_dump(self):
        data = {
            'id': 1,
            'email': 'email@test.com',
            'password': 'abcd1234',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = UserSchema()
        dumped = schema.dump(data).data

        self.assertFalse('id' in dumped)
        self.assertTrue('email' in dumped)
        self.assertFalse('password' in dumped)
        self.assertTrue('first_name' in dumped)
        self.assertTrue('last_name' in dumped)
        self.assertTrue('avatar' in dumped)
