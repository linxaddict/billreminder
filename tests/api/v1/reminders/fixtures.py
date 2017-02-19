from billreminder.api.v1.profile.models import User
from billreminder.api.v1.reminders.models import Reminder, ReminderDate

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


def user(email='test@mail.com', password='test_password', first_name='test_first_name',
         last_name='test_last_name'):
    return User.create(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )


def reminder_date(owner, reminder, date='2017-02-13T11:01:59+0000'):
    return ReminderDate.create(
        owner_id=owner.id,
        reminder_id=reminder.id,
        date=date
    )


# noinspection PyDefaultArgument
def reminder(owner, unit=12, value=23, start='2017-02-13T11:01:59+0000', end='2017-02-14T11:01:59+0000'):
    return Reminder.create(
        owner_id=owner.id,
        unit=unit,
        value=value,
        start=start,
        end=end
    )


# noinspection PyDefaultArgument
def reminder_dict(owner, dates=['2017-02-13T11:01:59+0000'], unit=12, value=23,
                  start='2017-02-13T11:01:59+0000', end='2017-02-14T11:01:59+0000'):
    return {
        'owner_id': owner.id,
        'unit': unit,
        'value': value,
        'start': start,
        'end': end,
        'dates': dates
    }
