import datetime as dt

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class Payment:
    def __init__(self, user, bill, created_at=None):
        self._user = user
        self._bill = bill
        self._created_at = created_at or dt.datetime.utcnow()

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def bill(self):
        return self._bill

    @bill.setter
    def bill(self, value):
        self._bill = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value


class Bill:
    def __init__(self, id, name, description=None, amount=None, last_payment=None, due_date=None,
                 repeat_mode=None, repeat_value=None, owner=None, payments=None,
                 participants=None):
        self._id = id
        self._name = name
        self._description = description
        self._amount = amount
        self._last_payment = last_payment
        self._due_date = due_date
        self._repeat_mode = repeat_mode
        self._repeat_value = repeat_value
        self._owner = owner
        self._payments = payments or []
        self._participants = participants or []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def last_payment(self):
        return self._last_payment

    @last_payment.setter
    def last_payment(self, value):
        self._last_payment = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        self._due_date = value

    @property
    def repeat_mode(self):
        return self._repeat_mode

    @repeat_mode.setter
    def repeat_mode(self, value):
        self._repeat_mode = value

    @property
    def repeat_value(self):
        return self._repeat_value

    @repeat_value.setter
    def repeat_value(self, value):
        self._repeat_value = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        self._owner = value

    @property
    def payments(self):
        return self._payments

    @payments.setter
    def payments(self, value):
        self._payments = value

    @property
    def participants(self):
        return self._participants

    @participants.setter
    def participants(self, value):
        self._participants = value
