from billreminder.api.v1.models import *
from billreminder.api.v1.bills.schemas import *
from billreminder.common.auth import AuthMixin
from billreminder.common.errors import ApiErrors
from billreminder.common.resources import RetrieveUpdateDestroyResource, ListCreateResource, BaseApiResource, \
    ListResource
from billreminder.extensions import api_v1, db
from billreminder.http_status import HTTP_200_OK
from billreminder.db.database import BillReminderDb

from datetime import datetime as dt

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


@api_v1.resource('/bills', strict_slashes=False)
class BillsView(AuthMixin, ListCreateResource):
    schema = BillSchema(strict=True)
    model = Bill

    def create_instance(self, instance):
        instance.participants.append(self.current_user)
        instance.owner = self.current_user

        super().create_instance(instance)

    @property
    def query(self):
        return super().query.filter(Bill.participants.any(User.id == self.current_user.id))


@api_v1.resource('/bills/<int:id>', strict_slashes=False)
class BillView(AuthMixin, RetrieveUpdateDestroyResource):
    schema = BillSchema(strict=True)
    model = Bill

    def has_access(self, instance):
        return self.current_user in instance.participants


@api_v1.resource('/bills/<int:id>/pay', strict_slashes=False)
class PaymentView(AuthMixin, BaseApiResource):
    def has_access(self, instance):
        if not instance:
            return True

        return self.current_user in instance.participants

    def post(self, id):
        from billreminder.model.bills import Bill, Payment
        # bill = Bill.query.filter(Bill.id == id).one_or_none()
        brdb = BillReminderDb(db)
        bill = brdb.fetch_by_id(Bill, id)
        if not bill:
            return ApiErrors.BILL_NOT_FOUND.value

        if not self.has_access(bill):
            return ApiErrors.ACCESS_DENIED.value

        payment = Payment(user=self.current_user, bill=bill)
        bill.last_payment = dt.now()
        brdb.update(bill)

        # db.session.add(payment)
        # db.session.commit()
        brdb.create(payment)

        return PaymentSchema().dump(payment).data, HTTP_200_OK


@api_v1.resource('/bills/<int:bill_id>/history', strict_slashes=False)
class PaymentHistory(AuthMixin, ListResource):
    schema = PaymentSchema(strict=True)
    model = Payment
    lookup_field = 'bill_id'

    def get(self, *args, **kwargs):
        bill = Bill.query.filter(Bill.id == kwargs['bill_id'])\
            .filter(Bill.owner_id == self.current_user.id).one_or_none()
        if not bill:
            b = Bill.query.filter(Bill.id == kwargs['bill_id']).one_or_none()
            if not b:
                return ApiErrors.BILL_NOT_FOUND.value
            else:
                return ApiErrors.ACCESS_DENIED.value

        return super().get(*args, **kwargs)
