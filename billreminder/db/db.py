from flask_sqlalchemy import SQLAlchemy

from billreminder.api.v1.bills.models import Bill as DbBill, Payment as DbPayment
from billreminder.model.bill import Bill, Payment

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class BillReminderDb:
    def validate_model(self, model):
        if model not in self._model_map:
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

    def fetch_all(self, model):
        db_model = self.db_model(model)
        return db_model.query.all()

    def fetch_by_id(self, model, id):
        db_model = self.db_model(model)
        return db_model.query.filter_by(id=id).one_or_none()
