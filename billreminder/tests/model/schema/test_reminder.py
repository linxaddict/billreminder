import datetime
from unittest import TestCase

from billreminder.model.db import Reminder, ReminderDate
from billreminder.model.schemas import ReminderSchema
from billreminder.settings import DATE_FORMAT

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestReminderSchema(TestCase):
    def test_load(self):
        data = {
            'unit': 1,
            'value': 12,
            'start': '2017-02-06T17:47:32+0100',
            'end': '2017-02-06T18:47:32+0100',
            'dates': [
                '2017-02-06T17:47:32+0100',
                '2017-02-06T18:47:32+0100'
            ]
        }

        schema = ReminderSchema()
        loaded, errors = schema.load(data)

        start = datetime.datetime.strptime(data['start'], DATE_FORMAT)
        end = datetime.datetime.strptime(data['end'], DATE_FORMAT)
        dates0 = datetime.datetime.strptime(data['dates'][0], DATE_FORMAT)
        dates1 = datetime.datetime.strptime(data['dates'][1], DATE_FORMAT)

        self.assertEqual(len(errors.keys()), 0)

        self.assertEqual(data['unit'], loaded.unit)
        self.assertEqual(data['value'], loaded.value)
        self.assertEqual(start, loaded.start)
        self.assertEqual(end, loaded.end)
        self.assertEqual(len(data['dates']), len(loaded.dates))
        self.assertEqual(dates0, loaded.dates[0].date)
        self.assertEqual(dates1, loaded.dates[1].date)

    def test_load_id_not_loaded(self):
        data = {
            'id': 1,
            'unit': 1,
            'value': 12,
            'start': '2017-02-06T17:47:32+0100',
            'end': '2017-02-06T18:47:32+0100',
            'dates': [
                '2017-02-06T17:47:32+0100',
                '2017-02-06T18:47:32+0100'
            ]
        }

        schema = ReminderSchema()
        loaded, errors = schema.load(data)

        self.assertFalse(loaded.id == data['id'])

    def test_load_start_bad_format(self):
        data = {
            'unit': 1,
            'value': 12,
            'start': '2017-02-06 17:47:32+0100',
            'end': '2017-02-06T18:47:32+0100',
            'dates': [
                '2017-02-06T17:47:32+0100',
                '2017-02-06T18:47:32+0100'
            ]
        }

        schema = ReminderSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('start' in errors)

    def test_load_end_bad_format(self):
        data = {
            'unit': 1,
            'value': 12,
            'start': '2017-02-06T17:47:32+0100',
            'end': '2017-02-06 18:47:32+0100',
            'dates': [
                '2017-02-06T17:47:32+0100',
                '2017-02-06T18:47:32+0100'
            ]
        }

        schema = ReminderSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('end' in errors)

    def test_load_dates_bad_format(self):
        data = {
            'unit': 1,
            'value': 12,
            'start': '2017-02-06T17:47:32+0100',
            'end': '2017-02-06T18:47:32+0100',
            'dates': [
                '2017-02-06 17:47:32+0100',
                '2017-02-06T18:47:32+0100'
            ]
        }

        schema = ReminderSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('dates' in errors)

    def test_load_start_missing(self):
        data = {
            'unit': 1,
            'value': 12,
            'end': '2017-02-06T18:47:32+0100',
            'dates': [
                '2017-02-06T17:47:32+0100',
                '2017-02-06T18:47:32+0100'
            ]
        }

        schema = ReminderSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('start' in errors)

    def test_dump(self):
        reminder_date_0 = ReminderDate()
        reminder_date_0.date = datetime.datetime.strptime('2017-02-06T17:47:32+0100', DATE_FORMAT)

        reminder_date_1 = ReminderDate()
        reminder_date_1.date = datetime.datetime.strptime('2017-02-06T17:47:32+0100', DATE_FORMAT)

        reminder = Reminder()
        reminder.id = 1
        reminder.unit = 4
        reminder.value = 12
        reminder.start = datetime.datetime.strptime('2017-02-06T17:47:32+0100', DATE_FORMAT)
        reminder.end = datetime.datetime.strptime('2017-02-06T18:47:32+0100', DATE_FORMAT)
        reminder.dates = [reminder_date_0, reminder_date_1]

        schema = ReminderSchema()
        dumped, errors = schema.dump(reminder)

        self.assertEqual(len(errors.keys()), 0)

        self.assertEqual(reminder.id, dumped['id'])
        self.assertEqual(reminder.unit, dumped['unit'])
        self.assertEqual(reminder.value, dumped['value'])
        self.assertEqual(reminder.start, datetime.datetime.strptime(dumped['start'], DATE_FORMAT))
        self.assertEqual(reminder.end, datetime.datetime.strptime(dumped['end'], DATE_FORMAT))

        self.assertEqual(reminder_date_0.date, datetime.datetime.strptime(dumped['dates'][0], DATE_FORMAT))
        self.assertEqual(reminder_date_1.date, datetime.datetime.strptime(dumped['dates'][1], DATE_FORMAT))
