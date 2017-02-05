from billreminder.common.auth import AuthMixin
from billreminder.common.errors import ApiErrors
from billreminder.common.resources import RetrieveUpdateDestroyResource, ListCreateResource, BaseApiResource
from billreminder.extensions import api_v1, db
from billreminder.http_status import HTTP_200_OK
from billreminder.model.db import Bill, Payment
from billreminder.model.schemas import BillSchema, PaymentSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


@api_v1.resource('/bills', strict_slashes=False)
class BillsView(AuthMixin, ListCreateResource):
    schema = BillSchema(strict=True)
    model = Bill

    def create_instance(self, instance):
        instance.participants.append(self.current_user)
        super().create_instance(instance)


@api_v1.resource('/bills/<int:id>', strict_slashes=False)
class BillView(AuthMixin, RetrieveUpdateDestroyResource):
    schema = BillSchema(strict=True)
    model = Bill

    def has_access(self, instance):
        return self.current_user in instance.participants


@api_v1.resource('/bills/<int:id>/pay', strict_slashes=False)
class PaymentView(AuthMixin, BaseApiResource):
    def post(self, id):
        bill = Bill.query.filter(Bill.id == id)
        if not bill:
            return ApiErrors.BILL_NOT_FOUND.value

        payment = Payment(user_id=self.current_user.id, bill_id=id)

        db.session.add(payment)
        db.session.commit()

        return PaymentSchema().dump(payment).data, HTTP_200_OK
