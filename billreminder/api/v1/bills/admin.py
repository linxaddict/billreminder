from flask_admin.contrib.sqla import ModelView

from billreminder.api.v1.bills.models import Bill, Payment
from billreminder.extensions import db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

models = [Bill, Payment]
views = [ModelView(model, db.session, category='Bills') for model in models]
