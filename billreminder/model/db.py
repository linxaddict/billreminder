import datetime as dt

from flask import current_app as app
from flask_login import UserMixin
from itsdangerous import SignatureExpired, BadSignature, JSONWebSignatureSerializer as Serializer
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from billreminder.database import Column, Model, SurrogatePK, db
from billreminder.extensions import bcrypt

from billreminder.api.v1.auth.models import User

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


users_bills = db.Table(
    'users_bills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('bill_id', db.Integer, db.ForeignKey('bills.id'))
)


class Bill(SurrogatePK, Model):
    __tablename__ = 'bills'

    name = Column(db.String, nullable=False)
    description = Column(db.String, nullable=False)
    amount = Column(db.Float, nullable=False)
    last_payment = Column(db.DateTime(timezone=True))

    owner_id = Column(db.Integer, ForeignKey('users.id'))
    payments = db.relationship('Payment', backref='bill')
    participants = db.relationship('User', secondary=users_bills,
                                   backref=db.backref('participants', lazy='dynamic'))


class Payment(SurrogatePK, Model):
    __tablename__ = 'payments'

    user_id = Column(Integer, ForeignKey('users.id'))
    bill_id = Column(Integer, ForeignKey('bills.id'))
    created_at = Column(db.DateTime(timezone=True), nullable=False, default=dt.datetime.utcnow)

    def __init__(self, user_id, bill_id, **kwargs):
        self.user_id = user_id
        self.bill_id = bill_id
