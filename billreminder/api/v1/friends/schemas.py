from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from billreminder.api.v1.friends.models import FriendRequest
from billreminder.api.v1.profile.schemas import UserSchema
from billreminder.extensions import db, ma

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class FriendRequestSchema(ModelSchema):
    class Meta:
        model = FriendRequest
        sqla_session = db.session
        exclude = ('from_user',)

    to_user = ma.Nested(UserSchema, dump_only=True, dump_to='user')
    created_at = fields.DateTime(dump_only=True)


class FriendSchema(ma.Schema):
    id = fields.Integer(load_only=True)
    email = fields.Email(required=True)
    first_name = fields.String()
    last_name = fields.String()
    avatar = fields.String()


class FriendInvitationSchema(ma.Schema):
    email = fields.Email(required=True)
