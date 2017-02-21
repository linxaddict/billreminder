from sqlalchemy import and_

import tests.api.v1.friends.fixtures as f
from billreminder.api.v1.friends.models import FriendRequest
from billreminder.api.v1.friends.schemas import FriendRequestSchema
from billreminder.http_status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
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
