from billreminder.api.v1.friends.models import FriendRequest
from billreminder.api.v1.profile.models import User

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


def user(email='test@mail.com', password='test_password', first_name='test_first_name',
         last_name='test_last_name', **kwargs):
    return User.create(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        **kwargs
    )


def friend_request(from_user=None, to_user=None):
    return FriendRequest.create(
        from_id=from_user.id,
        to_id=to_user.id
    )
