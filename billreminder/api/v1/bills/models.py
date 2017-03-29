import datetime as dt
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from billreminder.api.v1.profile.models import User
from billreminder.database import Column, Model, SurrogatePK, db
from billreminder.model.bills import Bill as PlainBill, Payment as PlainPayment

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

    def as_plain_object(self):
        return PlainPayment(user=self.user, bill=self.bill, created_at=self.create)

    @staticmethod
    def create_from(plain):
        return Payment.create(user_id=plain.user.id, bill_id=plain.bill.id,
                              created_at=plain.created_at)

    @staticmethod
    def update_with(plain):
        pass


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

    def as_plain_object(self):
        return PlainBill(id=self.id, name=self.name, description=self.description,
                         amount=self.amount, last_payment=self.last_payment, due_date=self.due_date,
                         repeat_mode=self.repeat_mode, repeat_value=self.repeat_value,
                         owner=self.owner, payments=self.payments, participants=self.participants)

    @staticmethod
    def create_from(plain):
        return Bill.create(id=plain.id, name=plain.name, description=plain.description,
                           amount=plain.amount, last_payment=plain.last_payment,
                           due_date=plain.due_date,
                           repeat_mode=plain.repeat_mode, repeat_value=plain.repeat_value,
                           owner=plain.owner, payments=plain.payments,
                           participants=plain.participants)

    @staticmethod
    def update_with(plain):
        bill = Bill.get_by_id(plain.id)

        if bill is not None:
            bill.name = plain.name
            bill.description = plain.description
            bill.amount = plain.amount
            bill.last_payment = plain.last_payment
            bill.due_date = plain.due_date
            bill.repeat_mode = plain.repeat_mode
            bill.owner = plain.owner
            bill.payments = plain.payments
            bill.participants = plain.participants

            bill.save()
