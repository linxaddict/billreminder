from flask import request, jsonify
from flask_restful import Resource

from billreminder.api.v1.auth.models import TokenResponse
from billreminder.api.v1.auth.schemas import LoginSchema, TokenResponseSchema
from billreminder.api.v1.profile.models import User
from billreminder.api.v1.profile.schemas import UserSchema
from billreminder.common.errors import ApiErrors
from billreminder.extensions import api_v1
from billreminder.extensions import db
from billreminder.http_status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
    HTTP_200_OK

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


@api_v1.resource('/auth/register', strict_slashes=False)
class RegistrationView(Resource):
    schema = UserSchema(strict=True)

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return ApiErrors.NO_INPUT_DATA.value

        user_data, errors = self.schema.load(request.get_json())

        existing_user = User.query.filter(User.email == user_data['email']).one_or_none()
        if existing_user:
            return ApiErrors.EMAIL_ALREADY_TAKEN.value

        if errors:
            return jsonify(errors), HTTP_400_BAD_REQUEST

        user = User(email=user_data['email'], password=user_data['password'],
                    first_name=user_data.get('first_name', None), last_name=user_data.get('last_name', None))

        db.session.add(user)
        db.session.commit()

        return self.schema.dump(user).data, HTTP_201_CREATED


@api_v1.resource('/auth/login', strict_slashes=False)
class LoginView(Resource):
    schema = LoginSchema(strict=True)
    token_schema = TokenResponseSchema(strict=True)

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return ApiErrors.NO_INPUT_DATA.value

        user_data, errors = self.schema.load(request.get_json())

        existing_user = User.query.filter(User.email == user_data['email']).one_or_none()
        if not existing_user:
            return ApiErrors.INVALID_EMAIL_OR_PASSWORD.value

        user = User.query.filter(User.email == user_data['email']).one_or_none()
        if not user.check_password(user_data['password']):
            return ApiErrors.INVALID_EMAIL_OR_PASSWORD.value

        return self.token_schema.dump(TokenResponse(user.generate_auth_token())).data, HTTP_200_OK
