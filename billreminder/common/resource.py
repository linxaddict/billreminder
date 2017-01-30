from functools import wraps

from flask import request
from flask_restful import Resource

from billreminder.http_status import HTTP_401_UNAUTHORIZED
from billreminder.model.db import User
from billreminder.model.schemas import PaginatedListSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


def auth_required(func):
    @wraps(func)
    def with_auth(*args, **kwargs):
        auth_token = request.headers.get(AuthResource.AUTH_TOKEN_HEADER, None)
        if not auth_token:
            return HTTP_401_UNAUTHORIZED

        user = User.verify_auth_token(auth_token)
        if not user:
            return HTTP_401_UNAUTHORIZED

        return func(*args, **kwargs)
    return with_auth


class AuthResource(Resource):
    AUTH_TOKEN_HEADER = 'Auth-Token'

    decorators = [auth_required]

    def __init__(self):
        super().__init__()
        self._current_user = None

    @property
    def current_user(self):
        if not self._current_user:
            auth_token = request.headers.get(self.AUTH_TOKEN_HEADER, None)
            if not auth_token:
                return HTTP_401_UNAUTHORIZED

            self._current_user = User.verify_auth_token(auth_token)

            return self._current_user
        else:
            return self._current_user


class PaginationMixin:
    QUERY_ARG_PAGE = 'page'
    DEFAULT_PAGE = 1
    ITEMS_PER_PAGE = 50

    paginated_schema = PaginatedListSchema(strict=True)
