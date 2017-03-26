from billreminder.api.v1.models import *
from billreminder.database import SurrogatePK, Model
from billreminder.extensions import db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class FriendRequest(SurrogatePK, Model):
    __tablename__ = 'friend_requests'

    from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=dt.datetime.utcnow)

    from_user = db.relationship('User', foreign_keys=[from_id])
    to_user = db.relationship('User', foreign_keys=[to_id])
