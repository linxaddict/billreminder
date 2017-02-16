from billreminder.extensions import db
from billreminder.model.db import User, Bill, Payment
import datetime as dt

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
