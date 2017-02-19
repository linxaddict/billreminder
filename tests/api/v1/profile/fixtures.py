from billreminder.api.v1.profile.models import User

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


def user_dict(email='test@mail.com', password='test_password', first_name='test_first_name',
              last_name='test_last_name'):
    return {
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name
    }


def user(email='test@mail.com', password='test_password', first_name='test_first_name',
         last_name='test_last_name'):
    return User.create(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
