from unittest import TestCase

from marshmallow import ValidationError

from billreminder.validation.validators import PasswordValidator

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class PasswordValidatorTest(TestCase):
    def test_validation(self):
        password = 'abcd1234'
        validator = PasswordValidator()

        self.assertEqual(password, validator(password))

    def test_validation_password_too_short(self):
        validator = PasswordValidator()

        with self.assertRaises(ValidationError):
            validator('abcd')
