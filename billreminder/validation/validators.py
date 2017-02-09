from marshmallow import ValidationError
from marshmallow.validate import Validator


__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class PasswordValidator(Validator):
    MIN_PASSWORD_LENGTH = 6

    def __call__(self, value):
        if len(value) < self.MIN_PASSWORD_LENGTH:
            raise ValidationError('password is too short, should be at least 6 characters long')

        return value
