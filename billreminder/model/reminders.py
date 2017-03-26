__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class ReminderDate:
    def __init__(self, reminder, date, owner):
        self._reminder = reminder
        self._date = date
        self._owner = owner

    @property
    def reminder(self):
        return self._reminder

    @reminder.setter
    def reminder(self, value):
        self._reminder = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        self._owner = value


class Reminder:
    def __init__(self, unit, value, start, end, owner):
        self._unit = unit
        self._value = value
        self._start = start
        self._end = end
        self._owner = owner

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value
