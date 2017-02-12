from marshmallow import fields
from marshmallow import post_dump
from marshmallow import pre_load
from marshmallow_sqlalchemy import ModelSchema

from billreminder.extensions import ma, db
from billreminder.model.db import ReminderDate, Reminder, Bill
from billreminder.settings import DATE_FORMAT
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


class ReminderDateSchema(ma.ModelSchema):
    class Meta:
        model = ReminderDate
        sqla_session = db.session
        fields = ('date',)

    date = fields.DateTime(format=DATE_FORMAT)

    @pre_load
    def wrap(self, reminder_date):
        return {'date': reminder_date}

    @post_dump
    def unwrap(self, reminder_date):
        return reminder_date['date']


class ReminderSchema(ma.ModelSchema):
    class Meta:
        model = Reminder
        sqla_session = db.session
        exclude = ('owner', 'owner_id')

    id = fields.Integer(dump_only=True)
    unit = fields.Integer(required=False)
    value = fields.Integer(required=False)
    start = fields.DateTime(required=True, format=DATE_FORMAT)
    end = fields.DateTime(required=False, format=DATE_FORMAT)
    dates = ma.List(ma.Nested(ReminderDateSchema), load_only=True)
    visible_dates = ma.List(ma.Nested(ReminderDateSchema), dump_only=True, dump_to='dates')


class PaymentSchema(ma.Schema):
    date = fields.DateTime(attribute='created_at', required=True, allow_none=False, format=DATE_FORMAT)


class BillSchema(ModelSchema):
    class Meta:
        model = Bill
        sqla_session = db.session

    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    amount = fields.Integer(required=True, validate=lambda n: n >= 0)
    last_payment = fields.DateTime(allow_none=True, format=DATE_FORMAT)
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
