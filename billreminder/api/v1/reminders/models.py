from enum import Enum

from sqlalchemy import ForeignKey

from billreminder.database import Column, Model, SurrogatePK, db, PlainModelMeta
from billreminder.model.reminders import Reminder as PlainReminder,\
    ReminderDate as PlainReminderDate

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class ReminderDate(SurrogatePK, Model, metaclass=PlainModelMeta):
    __tablename__ = 'reminder_dates'

    date = Column(db.DateTime(timezone=True), nullable=False)
    reminder = db.relationship('Reminder', backref=db.backref('dates', cascade='all, delete-orphan'))
    reminder_id = Column(db.Integer, ForeignKey('reminders.id'))
    owner_id = Column(db.Integer, ForeignKey('users.id'))

    # def as_plain_object(self):
    #     return PlainReminderDate(reminder=self.reminder, date=self.date, owner=self.owner)

    # @staticmethod
    # def create_from(plain):
    #     ReminderDate.create(data=plain.data, reminder=plain.reminder, owner_id=plain.owner.id)
    #
    # @staticmethod
    # def update_with(plain):
    #     reminder_date = ReminderDate.get_by_id(plain.id)
    #     reminder = Reminder.get_by_id(plain.reminder.id)
    #
    #     if reminder_date and reminder:
    #         reminder_date.date = plain.date
    #         reminder_date.reminder = reminder
    #         reminder_date.owner_id = plain.owner.id


class Reminder(SurrogatePK, Model):
    __tablename__ = 'reminders'

    class Unit(Enum):
        minute = 'minute'
        hour = 'hour'
        day = 'day'
        week = 'week'
        month = 'month'
        year = 'year'

    unit = Column(db.Enum(Unit), nullable=False)
    value = Column(db.Integer, nullable=False)
    start = Column(db.DateTime(timezone=True), nullable=False)
    end = Column(db.DateTime(timezone=True), nullable=False)
    owner_id = Column(db.Integer, ForeignKey('users.id'))

    @property
    def visible_dates(self):
        return [d for d in self.dates if d.owner_id == self.owner_id]

    def as_plain_object(self):
        return PlainReminder(unit=self.unit, value=self.value, start=self.start, end=self.end,
                             owner=self.owner)

    @staticmethod
    def create_from(plain):
        Reminder.create(unit=plain.unit, value=plain.value, start=plain.start, end=plain.end,
                        owner_id=plain.owner.id)

    @staticmethod
    def update_with(plain):
        reminder = Reminder.get_by_id(plain.id)

        if reminder:
            reminder.unit = plain.unit
            reminder.value = plain.value
            reminder.start = plain.start
            reminder.end = plain.end
            reminder.owner_id = plain.owner.id
