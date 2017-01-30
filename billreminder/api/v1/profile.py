from flask import request, jsonify

from billreminder.common.resource import AuthResource
from billreminder.http_status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_200_OK
from billreminder.model.schemas import UserSchema, UserUpdateSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class UserView(AuthResource):
    schema = UserSchema(strict=True)
    update_schema = UserUpdateSchema(strict=True)

    def get(self):
        return self.schema.dump(self.current_user).data

    def put(self):
        json_data = request.get_json()
        if not json_data:
            return {'error': 'No input data provided'}, HTTP_400_BAD_REQUEST

        allowed_fields = ('email', 'first_name', 'last_name')
        for k in [f for f in json_data if f not in allowed_fields]:
            json_data.pop(k, None)

        errors = self.update_schema.validate(json_data)
        if errors:
            return jsonify(errors), HTTP_422_UNPROCESSABLE_ENTITY

        self.current_user.update(**json_data)
        updated_user, errors = self.schema.dump(self.current_user)

        if errors:
            return jsonify(errors), HTTP_422_UNPROCESSABLE_ENTITY

        return updated_user, HTTP_200_OK
