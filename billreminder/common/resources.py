from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from billreminder.common.errors import ApiErrors
from billreminder.extensions import db
from billreminder.http_status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, \
    HTTP_201_CREATED
from billreminder.model.pagination import PaginatedList
from billreminder.model.schemas import create_paginated_list_schema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class BaseApiMixin:
    def has_access(self, instance):
        return True


class RetrieveMixin(BaseApiMixin):
    def retrieve(self, *args, **kwargs):
        try:
            entity = self.execute_query(**kwargs)

            if not self.has_access(entity):
                return ApiErrors.ACCESS_DENIED.value
        except NoResultFound:
            return ApiErrors.NO_RESULT_FOUND.value
        except MultipleResultsFound:
            return ApiErrors.MULTIPLE_RESULTS_FOUND.value

        return self.schema.dump(entity).data, HTTP_200_OK


class DestroyMixin(BaseApiMixin):
    def delete_instance(self, instance):
        db.session.delete(instance)
        db.session.commit()

    def destroy(self, *args, **kwargs):
        try:
            entity = self.execute_query(**kwargs)

            if not self.has_access(entity):
                return ApiErrors.ACCESS_DENIED.value
        except NoResultFound:
            return ApiErrors.NO_RESULT_FOUND.value
        except MultipleResultsFound:
            return ApiErrors.MULTIPLE_RESULTS_FOUND.value

        self.delete_instance(entity)

        return '', HTTP_204_NO_CONTENT


class UpdateMixin(BaseApiMixin):
    def update_instance(self, instance, json_data):
        instance.update(**json_data)

    def update(self, *args, **kwargs):
        try:
            entity = self.execute_query(**kwargs)

            if not self.has_access(entity):
                return ApiErrors.ACCESS_DENIED.value
        except NoResultFound:
            return ApiErrors.NO_RESULT_FOUND.value
        except MultipleResultsFound:
            return ApiErrors.MULTIPLE_RESULTS_FOUND.value

        json_data = request.get_json()
        errors = self.schema.validate(json_data, db.session)

        if errors:
            return jsonify(errors), HTTP_400_BAD_REQUEST

        self.update_instance(entity, json_data)

        return self.schema.dump(entity).data, HTTP_200_OK


class CreateMixin(BaseApiMixin):
    def create_instance(self, instance):
        db.session.add(instance)
        db.session.commit()

    def create(self, *args, **kwargs):
        json_data = request.get_json()
        entity, errors = self.schema.load(json_data)

        if errors:
            return jsonify(errors), HTTP_400_BAD_REQUEST

        self.create_instance(entity)

        return self.schema.dump(entity).data, HTTP_201_CREATED


class ListMixin(BaseApiMixin):
    QUERY_ARG_PAGE = 'page'
    DEFAULT_PAGE = 1
    ITEMS_PER_PAGE = 50

    def execute_query(self, *args, **kwargs):
        try:
            page = int(request.args.get(self.QUERY_ARG_PAGE, self.DEFAULT_PAGE))
        except ValueError:
            page = self.DEFAULT_PAGE

        if self.lookup_field:
            filter_kwargs = {self.lookup_field: kwargs[self.lookup_field]}
        else:
            filter_kwargs = {}

        return self.query.filter_by(**filter_kwargs).paginate(page, self.ITEMS_PER_PAGE)

    def retrieve(self, *args, **kwargs):
        entities = self.execute_query(*args, **kwargs)
        pagination_schema = create_paginated_list_schema(self.schema, strict=True)

        return pagination_schema.dump(PaginatedList(entities)).data


class BaseApiResource(Resource):
    schema = None
    model = None
    lookup_field = 'id'

    @property
    def query(self):
        return self.model.query

    def execute_query(self, *args, **kwargs):
        filter_kwargs = {self.lookup_field: kwargs[self.lookup_field]}
        return self.query.filter_by(**filter_kwargs).one()


class CreateResource(CreateMixin, BaseApiResource):
    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class RetrieveUpdateDestroyResource(RetrieveMixin, UpdateMixin, DestroyMixin, BaseApiResource):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.destroy(*args, **kwargs)


class ListResource(ListMixin, BaseApiResource):
    lookup_field = None

    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)


class ListCreateResource(CreateMixin, ListMixin, BaseApiResource):
    lookup_field = None

    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)
