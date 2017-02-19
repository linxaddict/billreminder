import datetime as dt

from flask import current_app as app
from flask_login import UserMixin
from itsdangerous import SignatureExpired, BadSignature, JSONWebSignatureSerializer as Serializer

from billreminder.api.v1.reminders.models import *
from billreminder.extensions import bcrypt

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class Role(SurrogatePK, Model):
    __tablename__ = 'roles'

    name = Column(db.String, unique=True, nullable=False)
    user_id = Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    __tablename__ = 'users'

    email = Column(db.String, unique=True, nullable=False)
    password = Column(db.Binary, nullable=True)
    created_at = Column(db.DateTime(timezone=True), nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String, nullable=True)
    last_name = Column(db.String, nullable=True)
    active = Column(db.Boolean, default=True)
    is_admin = Column(db.Boolean, default=False)
    avatar = Column(db.String, nullable=True)

    payments = db.relationship('Payment', backref='user')
    bills = db.relationship('Bill', backref='owner')
    reminders = db.relationship('Reminder', backref='owner')
    reminder_dates = db.relationship('ReminderDate', backref='owner')

    def __init__(self, email, password=None, first_name=None, last_name=None, **kwargs):
        db.Model.__init__(self, email=email, first_name=first_name, last_name=last_name, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

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

    @staticmethod
    def get_by_email(email):
        return db.session.query(User).filter(User.email == email).one_or_none()

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)
