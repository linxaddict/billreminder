from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from billreminder.extensions import ma, db
from billreminder.model.db import Role, ReminderDate, Reminder, Bill

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role


class UserSchema(ma.Schema):
    id = fields.Integer(load_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    first_name = fields.String()
    last_name = fields.String()
    avatar = fields.String()


class UserUpdateSchema(ma.Schema):
    email = fields.Email()
    first_name = fields.String()
    last_name = fields.String()


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class TokenResponseSchema(ma.Schema):
    token = fields.String(required=True)


class ReminderDateSchema(ma.ModelSchema):
    class Meta:
        model = ReminderDate


class ReminderSchema(ma.ModelSchema):
    class Meta:
        model = Reminder


class ParticipantSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'first_name', 'last_name')


class PaymentSchema(ma.Schema):
    date = fields.DateTime(attribute='created_at', allow_none=False)


class BillSchema(ModelSchema):
    class Meta:
        model = Bill
        sqla_session = db.session

    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    amount = fields.Integer(required=True, validate=lambda n: n >= 0)
    last_payment = fields.DateTime(allow_none=True)
    participants = ma.List(ma.Nested(UserSchema))
    payments = ma.List(ma.Nested(PaymentSchema))
    owner = ma.Nested(UserSchema)


class PaginationSchema(ma.Schema):
    page = fields.Integer(dump_only=True)
    has_next = fields.Boolean(dump_only=True)
    total = fields.Integer(dump_to='total_items', dump_only=True)


def create_paginated_list_schema(nested_schema, **kwargs):
    class PaginatedListSchema(ma.Schema):
        pagination = fields.Nested(PaginationSchema, dump_only=True)
        items = fields.Nested(nested_schema, many=True, dump_only=True)

    return PaginatedListSchema(**kwargs)
