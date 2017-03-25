import datetime as dt
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from billreminder.api.v1.profile.models import User
from billreminder.database import Column, Model, SurrogatePK, db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


users_bills = db.Table(
    'users_bills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('bill_id', db.Integer, db.ForeignKey('bills.id'))
)


class Payment(SurrogatePK, Model):
    __tablename__ = 'payments'

    user_id = Column(Integer, ForeignKey('users.id'))
    bill_id = Column(Integer, ForeignKey('bills.id'))
    created_at = Column(db.DateTime(timezone=True), nullable=False, default=dt.datetime.utcnow)

    def __init__(self, user_id=None, bill_id=None, **kwargs):
        self.user_id = user_id
        self.bill_id = bill_id


class Bill(SurrogatePK, Model):
    __tablename__ = 'bills'

    class RepeatMode(Enum):
        minute = 'minute'
        hour = 'hour'
        day = 'day'
        week = 'week'
        month = 'month'
        year = 'year'

    name = Column(db.String, nullable=False)
    description = Column(db.String, nullable=True)
    amount = Column(db.Float, nullable=True)
    last_payment = Column(db.DateTime(timezone=True), nullable=True)
    due_date = Column(db.DateTime(timezone=True), nullable=True)
    repeat_mode = Column(db.Enum(RepeatMode), nullable=True)
    repeat_value = Column(db.Integer, nullable=True)

    owner_id = Column(db.Integer, ForeignKey('users.id'))
    payments = db.relationship(Payment, backref='bill')
    participants = db.relationship(User, secondary=users_bills,
                                   backref=db.backref('participants', lazy='dynamic'))
