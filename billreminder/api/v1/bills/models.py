import datetime as dt

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

    def __init__(self, user_id, bill_id, **kwargs):
        self.user_id = user_id
        self.bill_id = bill_id


class Bill(SurrogatePK, Model):
    __tablename__ = 'bills'

    name = Column(db.String, nullable=False)
    description = Column(db.String, nullable=False)
    amount = Column(db.Float, nullable=False)
    last_payment = Column(db.DateTime(timezone=True))
    due_date = Column(db.DateTime(timezone=True), nullable=True)

    owner_id = Column(db.Integer, ForeignKey('users.id'))
    payments = db.relationship(Payment, backref='bill')
    participants = db.relationship(User, secondary=users_bills,
                                   backref=db.backref('participants', lazy='dynamic'))
