import os
import uuid

from flask import json
from flask import request, jsonify, current_app as app
from flask import send_from_directory

from billreminder.common.auth import AuthMixin
from billreminder.common.errors import ApiErrors
from billreminder.common.resources import BaseApiResource
from billreminder.extensions import api_v1
from billreminder.http_status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from billreminder.model.schemas import UserSchema, UserUpdateSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


@api_v1.resource('/profile', strict_slashes=False)
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


@api_v1.resource('/profile/photo', strict_slashes=False)
class PhotoView(AuthMixin, BaseApiResource):
    def post(self):
        files = request.files
        if not files or 'photo' not in files:
            return ApiErrors.NO_INPUT_DATA

        photo = request.files['photo']
        _, ext = os.path.splitext(photo.filename)

        photo_name = str(uuid.uuid4())
        if ext:
            photo_name = '{0}{1}'.format(photo_name, ext)

        photo.save(os.path.join(app.config['PHOTOS_DIR'], photo_name))

        url = request.url
        avatar_url = '{0}/{1}'.format(url, photo_name)

        self.current_user.update(avatar=avatar_url)

        return json.dumps({'filename': photo_name})


@api_v1.resource('/profile/photo/<string:name>', strict_slashes=False)
class FetchPhotoView(BaseApiResource):
    def get(self, name):
        return send_from_directory(os.path.join(os.getcwd(), app.config['PHOTOS_DIR']), name)
