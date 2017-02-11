import datetime
from unittest import TestCase

from billreminder.model.db import Bill
from billreminder.model.schemas import BillSchema
from billreminder.settings import DATE_FORMAT

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestBillSchema(TestCase):
    def test_load(self):
        data = {
            'name': 'test_name',
            'description': 'test_description',
            'amount': 12,
            'last_payment': '2017-02-06T17:47:32+0100'
        }

        schema = BillSchema()
        loaded, errors = schema.load(data)
        dt = datetime.datetime.strptime(data['last_payment'], DATE_FORMAT)

        self.assertEqual(len(errors.keys()), 0)

        self.assertEqual(data['name'], loaded.name)
        self.assertEqual(data['description'], loaded.description)
        self.assertEqual(data['amount'], loaded.amount)
        self.assertEqual(dt, loaded.last_payment)

    def test_load_id_not_loaded(self):
        data = {
            'id': 1,
            'name': 'test_name',
            'description': 'test_description',
            'amount': 12,
            'last_payment': '2017-02-06T17:47:32+0100'
        }

        schema = BillSchema()
        loaded, errors = schema.load(data)

        self.assertEqual(len(errors.keys()), 0)
        self.assertNotEqual(data['id'], loaded.id)

    def test_load_missing_name(self):
        data = {
            'description': 'test_description',
            'amount': 12,
            'last_payment': '2017-02-06T17:47:32+0100'
        }

        schema = BillSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('name' in errors)

    def test_load_missing_description(self):
        data = {
            'name': 'test_name',
            'amount': 12,
            'last_payment': '2017-02-06T17:47:32+0100'
        }

        schema = BillSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('description' in errors)

    def test_load_missing_amount(self):
        data = {
            'name': 'test_name',
            'description': 'test_description',
            'last_payment': '2017-02-06T17:47:32+0100'
        }

        schema = BillSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('amount' in errors)

    def test_load_amount_less_than_zero(self):
        data = {
            'name': 'test_name',
            'description': 'test_description',
            'amount': -1,
            'last_payment': '2017-02-06T17:47:32+0100'
        }

        schema = BillSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('amount' in errors)

    def test_load_invalid_date_format(self):
        data = {
            'name': 'test_name',
            'description': 'test_description',
            'amount': 12,
            'last_payment': '2017-02-06 17:47:32+0100'
        }

        schema = BillSchema()
        loaded, errors = schema.load(data)

        self.assertTrue('last_payment' in errors)

    def test_dump(self):
        bill = Bill()
        bill.id = 1
        bill.name = 'test_name'
        bill.description = 'test_description'
        bill.amount = 12
        bill.last_payment = datetime.datetime.strptime('2017-02-06T17:47:32+0100', DATE_FORMAT)

        schema = BillSchema()
        dumped = schema.dump(bill).data

        self.assertEqual(dumped['id'], bill.id)
        self.assertEqual(dumped['name'], bill.name)
        self.assertEqual(dumped['description'], bill.description)
        self.assertEqual(dumped['amount'], bill.amount)
        self.assertEqual(dumped['last_payment'], datetime.datetime.strftime(bill.last_payment, DATE_FORMAT))
