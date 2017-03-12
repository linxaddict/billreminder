from flask_admin.contrib.sqla import ModelView

from billreminder.api.v1.reminders.models import Reminder
from billreminder.api.v1.reminders.models import ReminderDate
from billreminder.extensions import db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

models = [Reminder, ReminderDate]
views = [ModelView(model, db.session, category='Reminders') for model in models]
