from flask import json
from sqlalchemy import and_

import tests.api.v1.friends.fixtures as f
from billreminder.api.v1.friends.models import FriendRequest
from billreminder.api.v1.friends.schemas import FriendRequestSchema, FriendSchema
from billreminder.api.v1.profile.models import User
from billreminder.http_status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from tests.base import BaseTest, ViewTestMixin

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class FriendRequestViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/friends/requests'

    def test_fetch(self):
        u1 = f.user(email='e1@mail.com')
        u2 = f.user(email='e2@mail.com')
        u3 = f.user(email='e3@mail.com')

        fr1 = f.friend_request(u1, self.current_user)
        fr2 = f.friend_request(u2, self.current_user)
        f.friend_request(self.current_user, u3)
        friend_requests = [fr1, fr2]

        response = self.client.get(self.url, content_type=self.json_content_type, headers=self.auth_header)
        schema = FriendRequestSchema()

        serialized = schema.dump(friend_requests, many=True).data

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(response.json['items'], serialized)

    def test_fetch_empty_list(self):
        response = self.client.get(self.url, content_type=self.json_content_type, headers=self.auth_header)
        schema = FriendRequestSchema()

        serialized = schema.dump([], many=True).data

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(response.json['items'], serialized)

    def test_fetch_unauthorized(self):
        response = self.client.get(self.url, content_type=self.json_content_type)
        self.assertStatus(response, HTTP_401_UNAUTHORIZED)


class AcceptFriendRequestViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/friends/requests/{id}/accept'

    def test_accept(self):
        u1 = f.user(email='e1@mail.com')
        u2 = f.user(email='e2@mail.com')

        f1 = f.friend_request(u1, self.current_user)
        f.friend_request(u2, self.current_user)

        url = self.url.format(id=f1.id)
        response = self.client.post(url, content_type=self.json_content_type, headers=self.auth_header)
        fr = FriendRequest.query.filter(and_(FriendRequest.from_id == u1.id,
                                             FriendRequest.to_id == self.current_user.id)).one_or_none()

        self.assertStatus(response, HTTP_204_NO_CONTENT)
        self.assertIsNone(fr)
        self.assertTrue(u1 in self.current_user.friends)

    def test_accept_invalid_id(self):
        url = self.url.format(id=1)
        response = self.client.post(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_404_NOT_FOUND)

    def test_accept_unauthorized(self):
        url = self.url.format(id=1)
        response = self.client.post(url, content_type=self.json_content_type)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)


class DeclineFriendRequestViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/friends/requests/{id}/decline'

    def test_decline(self):
        u1 = f.user(email='e1@mail.com')
        u2 = f.user(email='e2@mail.com')

        f1 = f.friend_request(u1, self.current_user)
        f.friend_request(u2, self.current_user)

        url = self.url.format(id=f1.id)
        response = self.client.post(url, content_type=self.json_content_type, headers=self.auth_header)
        fr = FriendRequest.query.filter(and_(FriendRequest.from_id == u1.id,
                                             FriendRequest.to_id == self.current_user.id)).one_or_none()

        self.assertStatus(response, HTTP_204_NO_CONTENT)
        self.assertIsNone(fr)
        self.assertFalse(u1 in self.current_user.friends)

    def test_decline_invalid_id(self):
        url = self.url.format(id=1)
        response = self.client.post(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_404_NOT_FOUND)

    def test_decline_unauthorized(self):
        url = self.url.format(id=1)
        response = self.client.post(url, content_type=self.json_content_type)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)


class FriendsViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/friends'

    def test_fetch(self):
        u1 = f.user(email='test1@mail.com')
        u2 = f.user(email='test2@mail.com')

        user = User.query.filter_by(id=self.current_user.id).one()
        user.friends.append(u1)
        user.friends.append(u2)

        response = self.client.get(self.url, headers=self.auth_header)
        serialized = FriendSchema(many=True).dump([u1, u2]).data

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(serialized, response.json['items'])

    def test_fetch_empty_list(self):
        response = self.client.get(self.url, headers=self.auth_header)
        serialized = FriendSchema(many=True).dump([]).data

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(serialized, response.json['items'])

    def test_fetch_unauthorized(self):
        response = self.client.get(self.url)
        self.assertStatus(response, HTTP_401_UNAUTHORIZED)

    def test_create(self):
        friend = f.user()
        data = {
            'email': friend.email
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type,
                                    headers=self.auth_header)
        friend_request = FriendRequest.query.one_or_none()

        self.assertStatus(response, HTTP_201_CREATED)
        self.assertIsNotNone(friend_request)
        self.assertEqual(friend_request.from_id, self.current_user.id)
        self.assertEqual(friend_request.to_id, friend.id)

    def test_create_unknown_email(self):
        data = {
            'email': 'a@b.com'
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_404_NOT_FOUND)

    def test_create_invalid_email(self):
        data = {
            'email': 'a@b.c'
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_create_email_missing(self):
        data = {}
        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_create_unauthorized(self):
        data = {}
        response = self.client.post(self.url, data=json.dumps(data), content_type=self.json_content_type)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)


class FriendViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/friends/{id}'

    def test_delete(self):
        u1 = f.user(email='test1@mail.com')
        u2 = f.user(email='test2@mail.com')

        user = User.query.filter_by(id=self.current_user.id).one()
        user.friends.append(u1)
        user.friends.append(u2)

        url = self.url.format(id=u1.id)
        response = self.client.delete(url, headers=self.auth_header)
        user = User.query.filter_by(id=self.current_user.id).one()

        friends = [fr.id for fr in user.friends]
        deleted_friend = User.query.filter_by(id=u1.id).one_or_none()

        self.assertStatus(response, HTTP_204_NO_CONTENT)
        self.assertFalse(u1.id in friends)
        self.assertIsNotNone(deleted_friend)

    def test_delete_invalid_id(self):
        url = self.url.format(id=1)
        response = self.client.delete(url, headers=self.auth_header)

        self.assertStatus(response, HTTP_404_NOT_FOUND)

    def test_delete_unauthorized(self):
        url = self.url.format(id=1)
        response = self.client.delete(url)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)
