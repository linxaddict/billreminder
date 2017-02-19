from unittest import TestCase

from billreminder.api.v1.auth.models import TokenResponse

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestTokenResponse(TestCase):
    def test_token(self):
        token = 'abcd'
        response = TokenResponse(token)

        self.assertEqual(token, response.token)
