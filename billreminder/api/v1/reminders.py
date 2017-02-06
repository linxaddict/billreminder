from billreminder.common.auth import AuthMixin
from billreminder.common.resources import ListCreateResource, RetrieveUpdateDestroyResource
from billreminder.extensions import api_v1
from billreminder.model.db import Reminder
from billreminder.model.schemas import ReminderSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


@api_v1.resource('/reminders', strict_slashes=False)
class RemindersView(AuthMixin, ListCreateResource):
    schema = ReminderSchema(strict=True)
    model = Reminder

    def create_instance(self, instance):
        instance.owner = self.current_user
        super().create_instance(instance)

    @property
    def query(self):
        return super().query.filter(Reminder.owner_id == self.current_user.id)


@api_v1.resource('/reminders/<int:id>', strict_slashes=False)
class ResourceView(AuthMixin, RetrieveUpdateDestroyResource):
    schema = ReminderSchema(strict=True)
    model = Reminder

    def has_access(self, instance):
        return self.current_user.id == instance.owner_id
