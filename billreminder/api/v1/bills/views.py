from billreminder.api.errors import NotFoundError, AccessDeniedError
from billreminder.api.v1.models import *
from billreminder.api.v1.bills.schemas import *
from billreminder.common.auth import AuthMixin
from billreminder.common.errors import ApiErrors
from billreminder.common.resources import RetrieveUpdateDestroyResource, ListCreateResource, BaseApiResource, \
    ListResource
from billreminder.extensions import api_v1
from billreminder.http_status import HTTP_200_OK

from datetime import datetime as dt

from billreminder.services import br_db

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
    def __init__(self):
        super().__init__()
        self.response = ApiErrors.BILL_NOT_FOUND.value

    def set_response(self, response):
        self.response = response

    def has_access(self, instance):
        if not instance:
            return True

        return self.current_user in instance.participants

    def map_to_payment(self, bill):
        from billreminder.model.bills import Payment

        if bill is None:
            raise NotFoundError()

        if not self.has_access(bill):
            raise AccessDeniedError()

        payment = Payment(user=self.current_user, bill=bill)
        bill.last_payment = dt.now()
        br_db.update(bill)
        br_db.create(payment)

        return payment

    def post(self, id):
        from billreminder.model.bills import Bill

        try:
            bill = br_db.fetch_by_id(Bill, id)
            payment = self.map_to_payment(bill)
        except NotFoundError:
            return ApiErrors.BILL_NOT_FOUND.value
        except AccessDeniedError:
            return ApiErrors.ACCESS_DENIED.value

        return PaymentSchema().dump(payment).data, HTTP_200_OK


@api_v1.resource('/bills/<int:bill_id>/history', strict_slashes=False)
class PaymentHistory(AuthMixin, ListResource):
    schema = PaymentSchema(strict=True)
    model = Payment
    lookup_field = 'bill_id'

    def get(self, *args, **kwargs):
        from billreminder.model.bills import Bill

        bill = br_db.fetch_by_id(Bill, kwargs['bill_id'])
        if not bill:
            return ApiErrors.BILL_NOT_FOUND.value

        if bill.owner.id != self.current_user.id:
            return ApiErrors.ACCESS_DENIED.value

        return super().get(*args, **kwargs)
