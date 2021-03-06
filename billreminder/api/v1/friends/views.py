from flask import request
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from billreminder.api.v1.friends.models import FriendRequest
from billreminder.api.v1.friends.schemas import FriendRequestSchema, FriendSchema, FriendInvitationSchema
from billreminder.api.v1.profile.models import User
from billreminder.common.auth import AuthMixin
from billreminder.common.errors import ApiErrors
from billreminder.common.resources import ListResource, CreateResource, ListCreateResource, DestroyResource
from billreminder.extensions import api_v1, db
from billreminder.http_status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

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

            db.session.query(FriendRequest).filter(and_(FriendRequest.from_id == entity.to_id,
                                                        FriendRequest.to_id == entity.from_id)).delete()
            self.current_user.befriend(entity.from_user)

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

            db.session.query(FriendRequest).filter(and_(FriendRequest.from_id == entity.to_id,
                                                        FriendRequest.to_id == entity.from_id)).delete()
            db.session.delete(entity)
            db.session.commit()

            return '', HTTP_204_NO_CONTENT
        except NoResultFound:
            return ApiErrors.NO_RESULT_FOUND.value


@api_v1.resource('/friends', strict_slashes=False)
class FriendsView(AuthMixin, ListCreateResource):
    schema = FriendSchema
    model = User

    @property
    def query(self):
        return User.query.filter(User.id.in_([f.id for f in self.current_user.friends]))

    def post(self, *args, **kwargs):
        schema = FriendInvitationSchema(strict=True)
        invitation, errors = schema.load(request.json)
        if errors:
            return ApiErrors.BAD_REQUEST.value

        user = db.session.query(User).filter_by(email=invitation['email']).one_or_none()
        if user is None:
            return ApiErrors.USER_NOT_FOUND.value

        fr = FriendRequest.create(from_id=self.current_user.id, to_id=user.id)
        fr.save()

        return schema.dump(invitation).data, HTTP_201_CREATED


@api_v1.resource('/friends/<int:id>', strict_slashes=False)
class FriendView(AuthMixin, DestroyResource):
    schema = FriendSchema
    model = User

    def delete_instance(self, instance):
        self.current_user.unfriend(instance)
        self.current_user.save()

    def delete(self, *args, **kwargs):
        friend = User.query.filter_by(id=kwargs['id']).one_or_none()
        if friend not in self.current_user.friends:
            return ApiErrors.USER_NOT_FOUND.value

        return super().delete(*args, **kwargs)


