import datetime as dt

from billreminder.api.v1.auth.models import User
from billreminder.api.v1.bills.models import Bill, Payment
from billreminder.api.v1.reminders.models import Reminder, ReminderDate
from billreminder.extensions import db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


def user_dict(email='test@mail.com', password='test_password', first_name='test_first_name',
              last_name='test_last_name'):
    return {
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name
    }


def user(email='test@mail.com', password='test_password', first_name='test_first_name',
         last_name='test_last_name'):
    return User.create(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )


def login_dict(email='test@mail.com', password='test_password'):
    return {
        'email': email,
        'password': password
    }


def bill_dict(name='test_bill', description='test_description', amount=12.4):
    return {
        'name': name,
        'description': description,
        'amount': amount
    }


def bill(owner, name='test_bill', description='test_description', amount=12.4, last_payment=dt.datetime.utcnow()):
    b = Bill.create(
        name=name,
        description=description,
        amount=amount,
        last_payment=last_payment,
        owner_id=owner.id
    )
    b.participants.append(owner)

    db.session.commit()

    return b


def payment(user_id=1, bill_id=1):
    return Payment.create(
        user_id=user_id,
        bill_id=bill_id
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
