from flask_admin.contrib.sqla import ModelView

from billreminder.api.v1.friends.models import Role
from billreminder.api.v1.profile.models import User
from billreminder.extensions import db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

models = [User, Role]
views = [ModelView(model, db.session, category='Users') for model in models]
