from marshmallow import ValidationError
from marshmallow import fields
from marshmallow import post_dump
from marshmallow import pre_load
from marshmallow import validates_schema

from billreminder.api.v1.reminders.models import ReminderDate, Reminder
from billreminder.extensions import ma, db
from billreminder.settings import DATE_FORMAT

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


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

    @validates_schema
    def validate_dates(self, data):
        if 'start' in data and 'end' in data and data['start'] >= data['end']:
            raise ValidationError(field_names=['start', 'end'], message='Start date must be before end date')


class PaginationSchema(ma.Schema):
    page = fields.Integer(dump_only=True)
    has_next = fields.Boolean(dump_only=True)
    total = fields.Integer(dump_to='total_items', dump_only=True)


def create_paginated_list_schema(nested_schema, **kwargs):
    class PaginatedListSchema(ma.Schema):
        pagination = fields.Nested(PaginationSchema, dump_only=True)
        items = fields.Nested(nested_schema, many=True, dump_only=True)

    return PaginatedListSchema(**kwargs)
