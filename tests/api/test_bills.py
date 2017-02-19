import json

from billreminder.api.v1.bills.models import Bill, Payment
from billreminder.extensions import db
from billreminder.http_status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from billreminder.model.schemas import BillSchema, PaymentSchema
from tests.api import fixtures as f
from tests.base import BaseTest, ViewTestMixin

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class BillsViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/bills'

    def test_fetch(self):
        bill = f.bill(self.current_user)

        response = self.client.get(self.url, content_type=self.json_content_type, headers=self.auth_header)
        serialized_bill = BillSchema().dump(bill).data

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(response.json['pagination']['total_items'], 1)
        self.assertEqual(response.json['items'][0], serialized_bill)

    def test_fetch_empty_list(self):
        response = self.client.get(self.url, content_type=self.json_content_type, headers=self.auth_header)
        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(response.json['pagination']['total_items'], 0)
        self.assertFalse(len(response.json['items']))

    def test_fetch_unauthorized(self):
        response = self.client.get(self.url, content_type=self.json_content_type)
        self.assertStatus(response, HTTP_401_UNAUTHORIZED)

    def test_create(self):
        bill_dict = f.bill_dict()
        response = self.client.post(self.url, data=json.dumps(bill_dict), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_201_CREATED)
        stored_bill = db.session.query(Bill).one_or_none()

        self.assertIsNotNone(stored_bill)
        self.assertEqual(bill_dict['name'], stored_bill.name)
        self.assertEqual(bill_dict['description'], stored_bill.description)
        self.assertEqual(bill_dict['amount'], stored_bill.amount)

    def test_create_no_input_data(self):
        response = self.client.post(self.url, data=json.dumps({}), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_create_missing_name(self):
        bill_dict = f.bill_dict()
        del bill_dict['name']

        response = self.client.post(self.url, data=json.dumps(bill_dict), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_create_missing_description(self):
        bill_dict = f.bill_dict()
        del bill_dict['description']

        response = self.client.post(self.url, data=json.dumps(bill_dict), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_create_missing_amount(self):
        bill_dict = f.bill_dict()
        del bill_dict['amount']

        response = self.client.post(self.url, data=json.dumps(bill_dict), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_create_amount_less_than_0(self):
        bill_dict = f.bill_dict()
        bill_dict['amount'] = -1

        response = self.client.post(self.url, data=json.dumps(bill_dict), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_create_unauthorized(self):
        bill_dict = f.bill_dict()
        self.token = None

        response = self.client.post(self.url, data=json.dumps(bill_dict), content_type=self.json_content_type,
                                    headers=self.auth_header)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)


class BillViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/bills/{id}'

    def test_fetch(self):
        bill = f.bill(owner=self.current_user)
        url = self.url.format(id=bill.id)

        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(BillSchema().dump(bill).data, response.json)

    def test_fetch_access_denied(self):
        user = f.user()
        bill = f.bill(user)
        url = self.url.format(id=bill.id)

        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_403_FORBIDDEN)

    def test_fetch_invalid_id(self):
        url = self.url.format(id=42)
        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_404_NOT_FOUND)

    def test_fetch_unauthorized(self):
        self.token = None
        url = self.url.format(id=42)
        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)

    def test_update(self):
        bill = f.bill(owner=self.current_user)
        url = self.url.format(id=bill.id)
        update_dict = f.bill_dict(name='n', description='d', amount=1.5)

        response = self.client.put(url, data=json.dumps(update_dict), content_type=self.json_content_type,
                                   headers=self.auth_header)

        updated_bill = db.session.query(Bill).one_or_none()
        schema = BillSchema()

        self.assertStatus(response, HTTP_200_OK)
        self.assertIsNotNone(updated_bill)
        self.assertEqual(schema.dump(updated_bill).data, response.json)
        self.assertEqual(update_dict['name'], updated_bill.name)
        self.assertEqual(update_dict['description'], updated_bill.description)
        self.assertEqual(update_dict['amount'], updated_bill.amount)

    def test_update_access_denied(self):
        user = f.user()
        bill = f.bill(owner=user)
        url = self.url.format(id=bill.id)

        response = self.client.put(url, data=json.dumps({}), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_403_FORBIDDEN)

    def test_update_no_input_data(self):
        bill = f.bill(owner=self.current_user)
        url = self.url.format(id=bill.id)

        response = self.client.put(url, data=json.dumps({}), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_400_BAD_REQUEST)

    def test_update_invalid_id(self):
        url = self.url.format(id=42)
        response = self.client.put(url, data=json.dumps(f.bill_dict()), content_type=self.json_content_type,
                                   headers=self.auth_header)

        self.assertStatus(response, HTTP_404_NOT_FOUND)

    def test_update_unauthorized(self):
        self.token = None
        url = self.url.format(id=42)

        response = self.client.put(url, data=json.dumps(f.bill_dict()), content_type=self.json_content_type)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)

    def test_delete(self):
        bill = f.bill(self.current_user)
        url = self.url.format(id=bill.id)

        response = self.client.delete(url, content_type=self.json_content_type, headers=self.auth_header)
        deleted_bill = Bill.get_by_id(bill.id)

        self.assertStatus(response, HTTP_204_NO_CONTENT)
        self.assertIsNone(deleted_bill)

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
        bill = f.bill(owner=user)
        url = self.url.format(id=bill.id)

        response = self.client.delete(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_403_FORBIDDEN)


class PaymentViewTest(ViewTestMixin, BaseTest):
    url = '/api/v1/bills/{id}/pay'

    def test_pay(self):
        bill = f.bill(owner=self.current_user)
        url = self.url.format(id=bill.id)

        response = self.client.post(url, content_type=self.json_content_type, headers=self.auth_header)
        payment = db.session.query(Payment).one_or_none()

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(payment.user_id, self.current_user.id)
        self.assertEqual(payment.bill_id, bill.id)

    def test_pay_access_denied(self):
        user = f.user()
        bill = f.bill(user)
        url = self.url.format(id=bill.id)

        response = self.client.post(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_403_FORBIDDEN)

    def test_pay_invalid_id(self):
        url = self.url.format(id=42)
        response = self.client.post(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_404_NOT_FOUND)

    def test_pay_unauthorized(self):
        self.token = None

        url = self.url.format(id=1)
        response = self.client.post(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)


class PaymentHistoryTest(ViewTestMixin, BaseTest):
    url = '/api/v1/bills/{id}/history'

    def test_fetch(self):
        bill = f.bill(self.current_user)
        payment = f.payment(self.current_user.id, bill.id)
        url = self.url.format(id=bill.id)

        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_200_OK)
        self.assertEqual(response.json['items'][0], PaymentSchema().dump(payment).data)

    def test_fetch_invalid_id(self):
        url = self.url.format(id=1)
        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_404_NOT_FOUND)

    def test_fetch_access_denied(self):
        user = f.user()
        bill = f.bill(user)
        f.payment(user.id, bill.id)
        url = self.url.format(id=bill.id)

        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_403_FORBIDDEN)

    def test_fetch_unauthorized(self):
        self.token = None
        url = self.url.format(id=1)
        response = self.client.get(url, content_type=self.json_content_type, headers=self.auth_header)

        self.assertStatus(response, HTTP_401_UNAUTHORIZED)
