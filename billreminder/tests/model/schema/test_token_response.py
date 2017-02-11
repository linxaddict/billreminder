from unittest import TestCase

from billreminder.model.schemas import TokenResponseSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestTokenResponse(TestCase):
    def test_load(self):
        data = {
            'token': 'test_token'
        }

        schema = TokenResponseSchema()
        loaded, errors = schema.load(data)

        self.assertEqual(len(errors.keys()), 0)
        self.assertEqual(data['token'], loaded['token'])

    def test_load_required(self):
        data = {
        }

        schema = TokenResponseSchema()
        loaded, errors = schema.load(data)

        self.assertEqual(len(loaded.keys()), 0)
        self.assertTrue('token' in errors)

    def test_dump(self):
        data = {
            'token': 'test_token'
        }

        schema = TokenResponseSchema()
        dumped = schema.dump(data).data

        self.assertEqual(data['token'], dumped['token'])
