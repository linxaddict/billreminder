__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class Payment:
    def __init__(self, user, bill, created_at, *args, **kwargs):
        self._user = user
        self._bill = bill
        self._created_at = created_at

    @property
    def user(self):
        return self._user

    @property
    def bill(self):
        return self._bill

    @property
    def created_at(self):
        return self._created_at


class Bill:
    def __init__(self, name, description=None, amount=None, last_payment=None, due_date=None,
                 repeat_mode=None, repeat_value=None, owner=None, payments=None,
                 participants=None):
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
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def amount(self):
        return self._amount

    @property
    def last_payment(self):
        return self._last_payment

    @property
    def due_date(self):
        return self._due_date

    @property
    def repeat_mode(self):
        return self._repeat_mode

    @property
    def repeat_value(self):
        return self._repeat_value

    @property
    def owner(self):
        return self._owner

    @property
    def payments(self):
        return self._payments

    @property
    def participants(self):
        return self._participants
