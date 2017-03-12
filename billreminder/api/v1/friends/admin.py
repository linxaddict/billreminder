from flask_admin.contrib.sqla import ModelView

from billreminder.api.v1.friends.models import FriendRequest
from billreminder.extensions import db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

models = [FriendRequest]
views = [ModelView(model, db.session, category='Friends') for model in models]
