from billreminder.common.auth import AuthMixin
from billreminder.common.resources import RetrieveUpdateDestroyResource, ListCreateResource
from billreminder.model.db import Bill
from billreminder.model.schemas import BillSchema
from billreminder.extensions import api_v1

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


@api_v1.resource('/bills', '/bills/')
class BillsView(AuthMixin, ListCreateResource):
    schema = BillSchema(strict=True)
    model = Bill


@api_v1.resource('/bills/<int:id>', '/bills/<int:id>/')
class BillView(AuthMixin, RetrieveUpdateDestroyResource):
    schema = BillSchema(strict=True)
    model = Bill
