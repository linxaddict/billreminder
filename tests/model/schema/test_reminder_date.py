import datetime
from unittest import TestCase

from billreminder.api.v1.reminders.models import ReminderDate
from billreminder.api.v1.reminders.schemas import ReminderDateSchema
from billreminder.settings import DATE_FORMAT

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestReminderDate(TestCase):
    def test_load(self):
        data = '2017-02-06T17:47:32+0100'

        schema = ReminderDateSchema()
        loaded, errors = schema.load(data)
        dt = datetime.datetime.strptime(data, DATE_FORMAT)

        self.assertEqual(len(errors.keys()), 0)
        self.assertEqual(dt, loaded.date)

    def test_load_bad_format(self):
        data = '2017-02-06 17:47:32+0100'

        schema = ReminderDateSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('date' in errors)

    def test_load_missing_date(self):
        data = ''

        schema = ReminderDateSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('date' in errors)

    def test_dump(self):
        date = '2017-02-06T17:47:32+0100'

        rd = ReminderDate()
        rd.date = datetime.datetime.strptime(date, DATE_FORMAT)

        schema = ReminderDateSchema()
        dumped = schema.dump(rd).data

        self.assertEqual(dumped, date)
