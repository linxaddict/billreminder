from unittest import TestCase

from billreminder.api.v1.friends.schemas import FriendSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestFriendSchema(TestCase):
    def test_load(self):
        data = {
            'id': 1,
            'email': 'email@test.com',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = FriendSchema()
        user = schema.load(data).data

        self.assertEqual(user['id'], data['id'])
        self.assertEqual(user['email'], data['email'])
        self.assertEqual(user['first_name'], data['first_name'])
        self.assertEqual(user['last_name'], data['last_name'])
        self.assertEqual(user['avatar'], data['avatar'])

    def test_load_invalid_email(self):
        data = {
            'id': 1,
            'email': 'email_test.com',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = FriendSchema()
        user, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('email' in errors)

    def test_load_empty_email(self):
        data = {
            'id': 1,
            'email': '',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = FriendSchema()
        user, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('email' in errors)

    def test_load_email_is_none(self):
        data = {
            'id': 1,
            'email': None,
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = FriendSchema()
        user, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('email' in errors)

    def test_load_only_required_fields_needed(self):
        data = {
            'email': 'email@test.com',
        }

        schema = FriendSchema()
        user, errors = schema.load(data)

        self.assertFalse(errors)

    def test_load_required_fields_missing(self):
        data = {
            'id': 1,
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = FriendSchema()
        user, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('email' in errors)

    def test_dump(self):
        data = {
            'id': 1,
            'email': 'email@test.com',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'avatar': 'http://avatar.com'
        }

        schema = FriendSchema()
        dumped = schema.dump(data).data

        self.assertFalse('id' in dumped)
        self.assertTrue('email' in dumped)
        self.assertTrue('first_name' in dumped)
        self.assertTrue('last_name' in dumped)
        self.assertTrue('avatar' in dumped)
