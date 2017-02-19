from marshmallow import fields

from billreminder.extensions import ma
from billreminder.validation.validators import PasswordValidator

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class UserSchema(ma.Schema):
    id = fields.Integer(load_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, validate=PasswordValidator())
    first_name = fields.String()
    last_name = fields.String()
    avatar = fields.String()


class UserUpdateSchema(ma.Schema):
    email = fields.Email()
    first_name = fields.String()
    last_name = fields.String()


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=PasswordValidator())


class TokenResponseSchema(ma.Schema):
    token = fields.String(required=True)
