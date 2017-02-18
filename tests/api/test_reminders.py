import json

import pytz

import tests.api.fixtures as f
from billreminder.extensions import db
from billreminder.http_status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from billreminder.model.db import Reminder
from billreminder.model.schemas import ReminderSchema
from billreminder.settings import DATE_FORMAT
from tests.base import BaseTest, ViewTestMixin

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class RemindersViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/reminders'

    def test_fetch(self):
        u = self.current_user
        r = f.reminder(u)
        rd = f.reminder_date(u, r)
        r.update(dates=[rd])

        response = self.client.get(self.url, content_type=self.json_content_type, headers=self.auth_header)
        returned_reminder = response.json['items'][0]
        schema = ReminderSchema()

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(returned_reminder, schema.dump(r).data)

    def test_fetch_empty_list(self):
        response = self.client.get(self.url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_200_OK)
        self.assertFalse(response.json['items'])

    def test_fetch_unauthorized(self):
        response = self.client.get(self.url, content_type=self.json_content_type)
        self.assertStatus(response, HTTP_401_UNAUTHORIZED)

    def test_create(self):
        reminder_dict = f.reminder_dict(self.current_user)

        response = self.client.post(self.url, data=json.dumps(reminder_dict), content_type=self.json_content_type,
                                    headers=self.auth_header)
        stored_reminder = db.session.query(Reminder).one_or_none()

        stored_reminder.start = stored_reminder.start.astimezone(pytz.utc)
        stored_reminder.end = stored_reminder.end.astimezone(pytz.utc)

        for reminder_date in stored_reminder.dates:
            reminder_date.date = reminder_date.date.astimezone(pytz.utc)

        schema = ReminderSchema()

        del reminder_dict['owner_id']
        reminder_dict['id'] = stored_reminder.id

        self.assertStatus(response, HTTP_201_CREATED)
        self.assertIsNotNone(stored_reminder)
        self.assertEqual(reminder_dict, schema.dump(stored_reminder).data)

    def test_create_duplicated_dates(self):
        reminder_dict = f.reminder_dict(self.current_user)
        reminder_dict['dates'] = ['2017-02-13T11:01:59+0000', '2017-02-13T11:01:59+0000', '2017-02-14T11:01:59+0000']

        response = self.client.post(self.url, data=json.dumps(reminder_dict), content_type=self.json_content_type,
                                    headers=self.auth_header)
        stored_reminder = db.session.query(Reminder).one_or_none()

        self.assertStatus(response, HTTP_201_CREATED)
        self.assertEqual(len(stored_reminder.dates), 2)

        d1 = stored_reminder.dates[0].date.astimezone(pytz.utc)
        d2 = stored_reminder.dates[1].date.astimezone(pytz.utc)

        self.assertTrue(d1.strftime(DATE_FORMAT) in reminder_dict['dates'])
        self.assertTrue(d2.strftime(DATE_FORMAT) in reminder_dict['dates'])

    def test_create_start_after_end(self):
        reminder_dict = f.reminder_dict(self.current_user, start='2017-02-14T11:01:59+0000',
                                        end='2017-02-13T11:01:59+0000')

        response = self.client.post(self.url, data=json.dumps(reminder_dict), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_create_start_equals_to_end(self):
        reminder_dict = f.reminder_dict(self.current_user, start='2017-02-14T11:01:59+0000',
                                        end='2017-02-14T11:01:59+0000')

        response = self.client.post(self.url, data=json.dumps(reminder_dict), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_create_empty_data(self):
        response = self.client.post(self.url, data=json.dumps({}), content_type=self.json_content_type,
                                    headers=self.auth_header)
        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_unauthorized(self):
        response = self.client.post(self.url, data=json.dumps({}), content_type=self.json_content_type)
        self.assertStatus(response, HTTP_401_UNAUTHORIZED)


class ReminderViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/reminders/{id}'

    def test_fetch(self):
        reminder = f.reminder(self.current_user)
        url = self.url.format(id=reminder.id)

        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)
        schema = ReminderSchema()

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(schema.dump(reminder).data, response.json)

    def test_fetch_invalid_id(self):
        url = self.url.format(id=1)
        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_404_NOT_FOUND)

    def test_fetch_unauthorized(self):
        url = self.url.format(id=1)
        response = self.client.get(url, content_type=self.json_content_type)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)

    def test_fetch_access_denied(self):
        user = f.user()
        reminder = f.reminder(owner=user)
        url = self.url.format(id=reminder.id)

        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_403_FORBIDDEN)

    def test_update(self):
        reminder = f.reminder(self.current_user)
        reminder_dict = f.reminder_dict(self.current_user, unit=14, value=15,
                                        dates=['2017-02-15T11:01:59+0000', '2017-06-15T11:01:59+0000'],
                                        start='2017-02-14T11:01:59+0000',
                                        end='2017-02-15T11:01:59+0000')
        url = self.url.format(id=reminder.id)
        response = self.client.put(url, data=json.dumps(reminder_dict), content_type=self.json_content_type,
                                   headers=self.auth_header)
        updated_reminder = db.session.query(Reminder).one_or_none()

        updated_reminder.start = updated_reminder.start.astimezone(pytz.utc)
        updated_reminder.end = updated_reminder.end.astimezone(pytz.utc)

        for reminder_date in updated_reminder.dates:
            reminder_date.date = reminder_date.date.astimezone(pytz.utc)

        schema = ReminderSchema()

        del reminder_dict['owner_id']
        reminder_dict['id'] = updated_reminder.id

        self.assertStatus(response, HTTP_200_OK)
        self.assertIsNotNone(updated_reminder)
        self.assertEqual(reminder_dict, schema.dump(updated_reminder).data)

    def test_update_duplicated_dates(self):
        reminder = f.reminder(self.current_user)
        reminder_dict = f.reminder_dict(self.current_user)
        reminder_dict['dates'] = ['2017-02-13T11:01:59+0000', '2017-02-13T11:01:59+0000', '2017-02-14T11:01:59+0000']

        url = self.url.format(id=reminder.id)
        response = self.client.put(url, data=json.dumps(reminder_dict), content_type=self.json_content_type,
                                   headers=self.auth_header)
        updated_reminder = db.session.query(Reminder).one_or_none()

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(len(updated_reminder.dates), 2)

        d1 = updated_reminder.dates[0].date.astimezone(pytz.utc)
        d2 = updated_reminder.dates[1].date.astimezone(pytz.utc)

        self.assertTrue(d1.strftime(DATE_FORMAT) in reminder_dict['dates'])
        self.assertTrue(d2.strftime(DATE_FORMAT) in reminder_dict['dates'])

    def test_update_start_after_end(self):
        reminder = f.reminder(self.current_user)
        reminder_dict = f.reminder_dict(self.current_user, unit=14, value=15,
                                        dates=['2017-02-15T11:01:59+0000', '2017-06-15T11:01:59+0000'],
                                        start='2017-02-16T11:01:59+0000',
                                        end='2017-02-15T11:01:59+0000')
        url = self.url.format(id=reminder.id)
        response = self.client.put(url, data=json.dumps(reminder_dict), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_update_start_equals_to_end(self):
        reminder = f.reminder(self.current_user)
        reminder_dict = f.reminder_dict(self.current_user, unit=14, value=15,
                                        dates=['2017-02-15T11:01:59+0000', '2017-06-15T11:01:59+0000'],
                                        start='2017-02-15T11:01:59+0000',
                                        end='2017-02-15T11:01:59+0000')
        url = self.url.format(id=reminder.id)
        response = self.client.put(url, data=json.dumps(reminder_dict), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_update_no_input_data(self):
        reminder = f.reminder(self.current_user)
        url = self.url.format(id=reminder.id)
        response = self.client.put(url, data=json.dumps({}), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_update_unauthorized(self):
        reminder = f.reminder(self.current_user)
        url = self.url.format(id=reminder.id)
        response = self.client.put(url, data=json.dumps({}), content_type=self.json_content_type)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)

    def test_update_access_denied(self):
        user = f.user()
        reminder = f.reminder(owner=user)
        url = self.url.format(id=reminder.id)

        response = self.client.put(url, data=json.dumps({}), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_403_FORBIDDEN)

    def test_delete(self):
        reminder = f.reminder(self.current_user)
        url = self.url.format(id=reminder.id)

        response = self.client.delete(url, content_type=self.json_content_type, headers=self.auth_header)
        deleted_reminder = db.session.query(Reminder).one_or_none()

        self.assertStatus(response, HTTP_204_NO_CONTENT)
        self.assertIsNone(deleted_reminder)

    def test_delete_invalid_id(self):
        url = self.url.format(id=1)
        response = self.client.delete(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_404_NOT_FOUND)

    def test_delete_unauthorized(self):
        url = self.url.format(id=1)
        response = self.client.delete(url, content_type=self.json_content_type)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)

    def test_delete_access_denied(self):
        user = f.user()
        reminder = f.reminder(owner=user)
        url = self.url.format(id=reminder.id)

        response = self.client.delete(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_403_FORBIDDEN)
