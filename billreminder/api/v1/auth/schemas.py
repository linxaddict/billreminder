from marshmallow import fields

from billreminder.extensions import ma
from billreminder.validation.validators import PasswordValidator

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=PasswordValidator())


class TokenResponseSchema(ma.Schema):
    token = fields.String(required=True)
