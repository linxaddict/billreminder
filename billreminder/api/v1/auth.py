from flask import request, jsonify
from flask_restful import Resource

from billreminder.extensions import db
from billreminder.http_status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED, \
    HTTP_409_CONFLICT
from billreminder.model.db import User
from billreminder.model.schemas import UserSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class RegistrationView(Resource):
    schema = UserSchema(strict=True)

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {'error': 'No input data provided'}, HTTP_400_BAD_REQUEST

        user_data, errors = self.schema.load(request.get_json())

        existing_user = User.query.filter(User.email == user_data['email']).first()
        if existing_user:
            return {'error': 'This e-mail address is already taken'}, HTTP_409_CONFLICT

        if errors:
            return jsonify(errors), HTTP_422_UNPROCESSABLE_ENTITY

        user = User(email=user_data['email'], password=user_data['password'],
                    first_name=user_data.get('first_name', None), last_name=user_data.get('last_name', None))

        db.session.add(user)
        db.session.commit()

        inserted_user, errors = self.schema.dump(user)

        if errors:
            return jsonify(errors), HTTP_422_UNPROCESSABLE_ENTITY

        return inserted_user, HTTP_201_CREATED
