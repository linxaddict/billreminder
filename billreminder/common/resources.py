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


class RetrieveMixin:
    def retrieve(self, *args, **kwargs):
        try:
            entity = self.execute_query(**kwargs)
        except NoResultFound:
            return ApiErrors.NO_RESULT_FOUND
        except MultipleResultsFound:
            return ApiErrors.MULTIPLE_RESULTS_FOUND

        return self.schema.dump(entity).data, HTTP_200_OK


class DestroyMixin:
    def destroy(self, *args, **kwargs):
        try:
            entity = self.execute_query(**kwargs)
        except NoResultFound:
            return ApiErrors.NO_RESULT_FOUND
        except MultipleResultsFound:
            return ApiErrors.MULTIPLE_RESULTS_FOUND

        db.session.delete(entity)
        db.session.commit()

        return HTTP_204_NO_CONTENT


class UpdateMixin:
    def update(self, *args, **kwargs):
        try:
            entity = self.execute_query(**kwargs)
        except NoResultFound:
            return ApiErrors.NO_RESULT_FOUND
        except MultipleResultsFound:
            return ApiErrors.MULTIPLE_RESULTS_FOUND

        json_data = request.get_json()
        errors = self.schema.validate(json_data, db.session)

        if errors:
            return jsonify(errors), HTTP_400_BAD_REQUEST

        entity.update(**json_data)

        return self.schema.dump(entity).data, HTTP_200_OK


class CreateMixin:
    def create(self, *args, **kwargs):
        json_data = request.get_json()
        entity, errors = self.schema.load(json_data)

        if errors:
            return jsonify(errors), HTTP_400_BAD_REQUEST

        db.session.add(entity)
        db.session.commit()

        return self.schema.dump(entity).data, HTTP_201_CREATED


class ListMixin:
    QUERY_ARG_PAGE = 'page'
    DEFAULT_PAGE = 1
    ITEMS_PER_PAGE = 50

    def retrieve(self, *args, **kwargs):
        try:
            page = int(request.args.get(self.QUERY_ARG_PAGE, self.DEFAULT_PAGE))
        except ValueError:
            page = self.DEFAULT_PAGE

        bills = self.model.query.paginate(page, self.ITEMS_PER_PAGE)
        pagination_schema = create_paginated_list_schema(self.schema, strict=True)

        return pagination_schema.dump(PaginatedList(bills)).data


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
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)


class ListCreateResource(CreateMixin, ListMixin, BaseApiResource):
    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)
