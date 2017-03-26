import datetime as dt

__author__ = 'Marcin  Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class FriendRequest:
    def __init__(self, from_user, to_user, created_at=None):
        self._from_user = from_user
        self._to_user = to_user
        self._created_at = created_at or dt.datetime.utcnow()

    @property
    def from_user(self):
        return self._from_user

    @from_user.setter
    def from_user(self, value):
        self._from_user = value

    @property
    def to_user(self):
        return self._to_user

    @to_user.setter
    def to_user(self, value):
        self._to_user = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value
