import datetime
from unittest import TestCase

from billreminder.model.schemas import PaymentSchema
from billreminder.settings import DATE_FORMAT

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestPaymentSchema(TestCase):
    def test_load(self):
        data = {
            'date': '2017-02-06T17:47:32+0100'
        }

        schema = PaymentSchema()
        loaded, errors = schema.load(data)
        dt = datetime.datetime.strptime(data['date'], DATE_FORMAT)

        self.assertEqual(len(errors.keys()), 0)
        self.assertEqual(dt, loaded['created_at'])

    def test_load_bad_format(self):
        data = {
            'date': '2017-02-06 17:47:32+0100'
        }

        schema = PaymentSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('date' in errors)

    def test_load_date_missing(self):
        data = {}

        schema = PaymentSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('date' in errors)

    def test_dump(self):
        data = {
            'date': '2017-02-06T17:47:32+0100'
        }

        schema = PaymentSchema()
        dumped = schema.load(data).data
        dt = datetime.datetime.strptime(data['date'], DATE_FORMAT)

        self.assertEqual(dt, dumped['created_at'])
