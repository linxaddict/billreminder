from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from billreminder.extensions import ma, db
from billreminder.model.models import Role, ReminderDate, Reminder, Bill


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role


class UserSchema(ma.ModelSchema):
    username = fields.String(required=False)
    email = fields.Email()
    created_at = fields.DateTime()
    first_name = fields.String()
    last_name = fields.String()


class ReminderDateSchema(ma.ModelSchema):
    class Meta:
        model = ReminderDate


class ReminderSchema(ma.ModelSchema):
    class Meta:
        model = Reminder


class ParticipantSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'first_name', 'last_name')


class BillSchema(ModelSchema):
    class Meta:
        model = Bill
        sqla_session = db.session

    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    amount = fields.Integer(required=True, validate=lambda n: n >= 0)
    last_payment = fields.DateTime(allow_none=True)
    participants = ma.List(ma.Nested(ParticipantSchema))


role_schema = RoleSchema()
user_schema = UserSchema()
reminder_date_schema = ReminderDateSchema()
reminder_schema = ReminderSchema()
participant_schema = ParticipantSchema()
bill_schema = BillSchema()
