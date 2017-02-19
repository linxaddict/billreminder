from sqlalchemy.orm.exc import NoResultFound

from billreminder.api.v1.friends.models import FriendRequest
from billreminder.api.v1.friends.schemas import FriendRequestSchema
from billreminder.common.auth import AuthMixin
from billreminder.common.errors import ApiErrors
from billreminder.common.resources import ListResource, CreateResource
from billreminder.extensions import api_v1, db
from billreminder.http_status import HTTP_204_NO_CONTENT

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


@api_v1.resource('/friends/requests', strict_slashes=False)
class FriendRequestsView(AuthMixin, ListResource):
    schema = FriendRequestSchema(strict=True)
    model = FriendRequest

    @property
    def query(self):
        return super().query.filter(FriendRequest.to_id == self.current_user.id)


@api_v1.resource('/friends/requests/<int:id>/accept', strict_slashes=False)
class AcceptFriendRequestView(AuthMixin, CreateResource):
    schema = FriendRequestSchema
    model = FriendRequest

    def has_access(self, instance):
        return instance.to_id == self.current_user.id

    def post(self, *args, **kwargs):
        try:
            entity = self.execute_query(**kwargs)

            if not self.has_access(entity):
                return ApiErrors.ACCESS_DENIED.value

            self.current_user.befriend(entity.from_user)
            # todo: remove symmetric request <3, 4> : <4, 3>

            db.session.delete(entity)
            db.session.commit()

            return '', HTTP_204_NO_CONTENT
        except NoResultFound:
            return ApiErrors.NO_RESULT_FOUND.value


@api_v1.resource('/friends/requests/<int:id>/decline', strict_slashes=False)
class DeclineFriendRequestView(AuthMixin, CreateResource):
    schema = FriendRequestSchema
    model = FriendRequest

    def has_access(self, instance):
        return instance.to_id == self.current_user.id

    def post(self, *args, **kwargs):
        try:
            entity = self.execute_query(**kwargs)

            if not self.has_access(entity):
                return ApiErrors.ACCESS_DENIED.value

            db.session.delete(entity)
            db.session.commit()

            return '', HTTP_204_NO_CONTENT
        except NoResultFound:
            return ApiErrors.NO_RESULT_FOUND.value
