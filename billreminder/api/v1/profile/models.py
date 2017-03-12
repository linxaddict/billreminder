import datetime as dt

from flask import current_app as app
from flask_login import UserMixin
from itsdangerous import SignatureExpired, BadSignature, JSONWebSignatureSerializer as Serializer
from sqlalchemy import ForeignKey

from billreminder.extensions import bcrypt
from billreminder.database import Column, Model, SurrogatePK, db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

friendships = db.Table(
    'friendships',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


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

    id = db.Column(db.Integer, primary_key=True)
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

    friends = db.relationship('User', secondary=friendships, primaryjoin=id == friendships.c.user_id,
                              secondaryjoin=id == friendships.c.friend_id)

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

    def befriend(self, user):
        if user.id != self.id and user not in self.friends:
            self.friends.append(user)
            user.friends.append(self)

    def unfriend(self, user):
        if user in self.friends:
            self.friends.remove(user)

        if self in user.friends:
            user.friends.remove(self)

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
        return '<User({email!r})>'.format(email=self.email)

    def __str__(self, *args, **kwargs):
        return self.email
