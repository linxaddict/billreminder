from flask_sqlalchemy import SQLAlchemy

from billreminder.api.v1.bills.models import Bill as DbBill, Payment as DbPayment
from billreminder.model.bills import Bill, Payment
import rx
from rx import Observer, Observable

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class BillReminderDb:
    def validate_model(self, model):
        if model not in self._model_map.keys():
            raise KeyError('Specified model not present in the model map')

    def db_model(self, model):
        self.validate_model(model)
        return self._model_map[model]

    def __init__(self, db: SQLAlchemy):
        self._db = db
        self._model_map = {
            Bill: DbBill,
            Payment: DbPayment
        }

    def update(self, instance):
        db_model = self.db_model(instance.__class__)
        db_model.update_with(plain=instance)

    def create(self, instance):
        db_model = self.db_model(instance.__class__)
        db_model.create_from(instance)

    def fetch_all(self, model) -> Observable:
        db_model = self.db_model(model)
        return Observable.from_([instance.as_plain_object() for instance in db_model.query.all()])

    def fetch_by_id(self, model, id) -> Observable:
        db_model = self.db_model(model)
        instance = db_model.query.filter_by(id=id).one_or_none()

        if instance is not None:
            instance = instance.as_plain_object()

        return Observable.just(instance)
