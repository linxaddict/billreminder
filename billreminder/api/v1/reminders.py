from billreminder.common.auth import AuthMixin
from billreminder.common.resources import ListCreateResource, RetrieveUpdateDestroyResource
from billreminder.extensions import api_v1
from billreminder.http_status import HTTP_400_BAD_REQUEST
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

        for date in instance.dates:
            date.owner = self.current_user

        super().create_instance(instance)

    @property
    def query(self):
        return super().query.filter(Reminder.owner_id == self.current_user.id)


@api_v1.resource('/reminders/<int:id>', strict_slashes=False)
class ResourceView(AuthMixin, RetrieveUpdateDestroyResource):
    schema = ReminderSchema(strict=True)
    model = Reminder

    def update_instance(self, instance, json_data):
        update_schema = ReminderSchema(exclude=('id', 'visible_dates'))

        loaded, errors = self.schema.load(json_data)
        if errors:
            return errors, HTTP_400_BAD_REQUEST

        new_dates = loaded.dates
        for d in new_dates:
            d.owner = self.current_user

        dumped, errors = update_schema.dump(loaded)
        if errors:
            return errors, HTTP_400_BAD_REQUEST

        instance.update(dates=new_dates, **dumped)

    def has_access(self, instance):
        return self.current_user.id == instance.owner_id
