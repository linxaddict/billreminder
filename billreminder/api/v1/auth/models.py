__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TokenResponse:
    def __init__(self, token):
        self._token = token

    @property
    def token(self):
        return self._token
