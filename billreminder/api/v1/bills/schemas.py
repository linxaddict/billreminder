from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from billreminder.api.v1.bills.models import Bill
from billreminder.api.v1.profile.schemas import UserSchema
from billreminder.extensions import ma, db
from billreminder.settings import DATE_FORMAT

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class PaymentSchema(ma.Schema):
    date = fields.DateTime(attribute='created_at', required=True, allow_none=False, format=DATE_FORMAT)


class BillSchema(ModelSchema):
    class Meta:
        model = Bill
        sqla_session = db.session

    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    amount = fields.Float(required=True, validate=lambda n: n >= 0)
    last_payment = fields.DateTime(allow_none=True, format=DATE_FORMAT)
    due_date = fields.DateTime(allow_none=True, format=DATE_FORMAT)
    participants = ma.List(ma.Nested(UserSchema))
    payments = ma.List(ma.Nested(PaymentSchema))
    owner = ma.Nested(UserSchema)
