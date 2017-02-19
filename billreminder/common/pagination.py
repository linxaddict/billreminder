from marshmallow import fields

from billreminder.extensions import ma

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class PaginationSchema(ma.Schema):
    page = fields.Integer(dump_only=True)
    has_next = fields.Boolean(dump_only=True)
    total = fields.Integer(dump_to='total_items', dump_only=True)


def create_paginated_list_schema(nested_schema, **kwargs):
    class PaginatedListSchema(ma.Schema):
        pagination = fields.Nested(PaginationSchema, dump_only=True)
        items = fields.Nested(nested_schema, many=True, dump_only=True)

    return PaginatedListSchema(**kwargs)


class Pagination:
    def __init__(self, paginated_items):
        self._has_next = paginated_items.has_next
        self._page = paginated_items.page
        self._total = paginated_items.total

    @property
    def has_next(self):
        return self._has_next

    @property
    def page(self):
        return self._page

    @property
    def total(self):
        return self._total


class PaginatedList:
    def __init__(self, paginated_items):
        self._items = paginated_items.items
        self._pagination = Pagination(paginated_items)

    @property
    def pagination(self):
        return self._pagination

    @property
    def items(self):
        return self._items
