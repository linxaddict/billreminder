import datetime as dt

import sqlalchemy
from flask_login import UserMixin
from flask import current_app as app
from itsdangerous import SignatureExpired, BadSignature, JSONWebSignatureSerializer as Serializer

from billreminder.database import Column, Model, SurrogatePK, db, reference_col, relationship
from billreminder.extensions import bcrypt

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class Role(SurrogatePK, Model):
    __tablename__ = 'roles'

    name = Column(db.String, unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    __tablename__ = 'users'

    email = Column(db.String, unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary, nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String, nullable=True)
    last_name = Column(db.String, nullable=True)
    active = Column(db.Boolean, default=True)
    is_admin = Column(db.Boolean, default=False)

    def __init__(self, email, password=None, first_name=None, last_name=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, email=email, first_name=first_name, last_name=last_name, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps(str(self.id))

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        user = User.query.get(data['id'])

        return user

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


class ReminderDate(SurrogatePK, Model):
    __tablename__ = 'reminder_dates'

    data = Column(db.DateTime, nullable=False)
    reminder = relationship('Reminder', backref='dates')
    reminder_id = reference_col('reminders', nullable=True)


class Reminder(SurrogatePK, Model):
    __tablename__ = 'reminders'

    unit = Column(db.Integer, nullable=False)
    value = Column(db.Integer, nullable=False)
    start = Column(db.DateTime, nullable=False)
    end = Column(db.DateTime, nullable=False)


class Participant(SurrogatePK, Model):
    __tablename__ = 'participants'

    first_name = Column(db.String, nullable=False)
    last_name = Column(db.String)


participants_bills = db.Table(
    'participants_bills',
    db.Column('participant_id', db.Integer, db.ForeignKey('participants.id')),
    db.Column('bill_id', db.Integer, db.ForeignKey('bills.id'))
)


class Bill(SurrogatePK, Model):
    __tablename__ = 'bills'

    name = Column(db.String, nullable=False)
    description = Column(db.String, nullable=False)
    amount = Column(db.Integer, nullable=False)
    last_payment = Column(db.DateTime)

    participants = db.relationship('Participant', secondary=participants_bills,
                                   backref=db.backref('participants', lazy='dynamic'))


class Author(Model):
    __tablename__ = 'authors'
    id = Column(sqlalchemy.Integer, primary_key=True)
    name = Column(sqlalchemy.String)

    def __repr__(self):
        return '<Author(name={self.name!r})>'.format(self=self)
