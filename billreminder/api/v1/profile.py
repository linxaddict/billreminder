from flask import request, jsonify

from billreminder.common.resources import BaseApiResource
from billreminder.common.auth import AuthMixin
from billreminder.http_status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from billreminder.model.schemas import UserSchema, UserUpdateSchema
from billreminder.extensions import api_v1

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


@api_v1.resource('/profile', '/profile/')
class UserView(AuthMixin, BaseApiResource):
    schema = UserSchema(strict=True)
    update_schema = UserUpdateSchema(strict=True)

    def get(self):
        return self.schema.dump(self.current_user).data

    def put(self):
        json_data = request.get_json()

        allowed_fields = ('email', 'first_name', 'last_name')
        for k in [f for f in json_data if f not in allowed_fields]:
            json_data.pop(k, None)

        errors = self.update_schema.validate(json_data)
        if errors:
            return jsonify(errors), HTTP_400_BAD_REQUEST

        self.current_user.update(**json_data)

        return self.schema.dump(self.current_user).data, HTTP_200_OK
