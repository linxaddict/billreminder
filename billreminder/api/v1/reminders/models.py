from sqlalchemy import ForeignKey

from billreminder.database import Column, Model, SurrogatePK, db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class ReminderDate(SurrogatePK, Model):
    __tablename__ = 'reminder_dates'

    date = Column(db.DateTime(timezone=True), nullable=False)
    reminder = db.relationship('Reminder', backref=db.backref('dates', cascade='all, delete-orphan'))
    reminder_id = Column(db.Integer, ForeignKey('reminders.id'))
    owner_id = Column(db.Integer, ForeignKey('users.id'))


class Reminder(SurrogatePK, Model):
    __tablename__ = 'reminders'

    unit = Column(db.Integer, nullable=False)
    value = Column(db.Integer, nullable=False)
    start = Column(db.DateTime(timezone=True), nullable=False)
    end = Column(db.DateTime(timezone=True), nullable=False)
    owner_id = Column(db.Integer, ForeignKey('users.id'))

    @property
    def visible_dates(self):
        return [d for d in self.dates if d.owner_id == self.owner_id]
