from unittest import TestCase

from billreminder.model.schemas import LoginSchema


__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestLoginSchema(TestCase):
    def test_load(self):
        data = {
            'email': 'test@email.com',
            'password': 'password1234'
        }

        schema = LoginSchema()
        loaded = schema.load(data).data

        self.assertTrue('email' in loaded)
        self.assertEqual(data['email'], loaded['email'])
        self.assertTrue('password' in loaded)
        self.assertTrue(data['password'], loaded['password'])

    def test_load_invalid_email(self):
        data = {
            'email': 'test_email.com',
            'password': 'password1234'
        }

        schema = LoginSchema()
        loaded, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('email' in errors)

    def test_load_empty_email(self):
        data = {
            'email': '',
            'password': 'password1234'
        }

        schema = LoginSchema()
        loaded, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('email' in errors)

    def test_load_empty_password(self):
        data = {
            'email': 'test@gmail.com',
            'password': ''
        }

        schema = LoginSchema()
        loaded, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('password' in errors)

    def test_load_password_too_short(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'abcd1'
        }

        schema = LoginSchema()
        loaded, errors = schema.load(data)

        self.assertIsNotNone(errors)
        self.assertTrue('password' in errors)

    def test_dump(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'abcd1234'
        }

        schema = LoginSchema()
        dumped = schema.dump(data).data

        self.assertEqual(data['email'], dumped['email'])
        self.assertEqual(data['password'], dumped['password'])
