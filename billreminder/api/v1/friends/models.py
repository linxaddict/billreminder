from billreminder.api.v1.models import *
from billreminder.database import SurrogatePK, Model
from billreminder.extensions import db
from billreminder.model.friends import FriendRequest as PlainFriendRequest

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class FriendRequest(SurrogatePK, Model):
    __tablename__ = 'friend_requests'

    from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=dt.datetime.utcnow)

    from_user = db.relationship('User', foreign_keys=[from_id])
    to_user = db.relationship('User', foreign_keys=[to_id])

    def as_plain_object(self):
        return PlainFriendRequest(from_user=self.from_user, to_user=self.to_user,
                                  created_at=self.created_at)

    @staticmethod
    def create_from(plain):
        return FriendRequest.create(from_user=plain.from_user, to_user=plain.to_user,
                                    created_at=plain.created_at)

    @staticmethod
    def update_with(plain):
        request = FriendRequest.get_by_id(plain.id)

        if request is not None:
            request.from_user = plain.from_user
            request.to_user = plain.to_user
            request.created_at = plain.created_at

            request.save()
