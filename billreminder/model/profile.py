import datetime as dt

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class Role:
    def __init__(self, name, user):
        self._name = name
        self._user = user

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value


class User:
    def __init__(self, id, email, password, created_at=None, first_name=None, last_name=None,
                 active=True, is_admin=False, avatar=None, payments=None, bills=None,
                 reminders=None, reminder_dates=None, friends=None):
        self._id = id
        self._email = email
        self._password = password
        self._created_at = created_at or dt.datetime.utcnow()
        self._first_name = first_name
        self._last_name = last_name
        self._active = active
        self._is_admin = is_admin
        self._avatar = avatar
        self._payments = payments
        self._bills = bills
        self._reminders = reminders
        self._reminder_dates = reminder_dates
        self._friends = friends

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def created_at(self):
        return self.created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        self._is_admin = value

    @property
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, value):
        self._avatar = value

    @property
    def payments(self):
        return self._payments

    @payments.setter
    def payments(self, value):
        self._payments = value

    @property
    def bills(self):
        return self._bills

    @bills.setter
    def bills(self, value):
        self._bills = value

    @property
    def reminders(self):
        return self._reminders

    @reminders.setter
    def reminders(self, value):
        self._reminders = value

    @property
    def reminder_dates(self):
        return self._reminder_dates

    @reminder_dates.setter
    def reminder_dates(self, value):
        self._reminder_dates = value

    @property
    def friends(self):
        return self._friends

    @friends.setter
    def friends(self, value):
        self._friends = value
