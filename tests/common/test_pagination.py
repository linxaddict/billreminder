from collections import namedtuple
from unittest import TestCase

from billreminder.api.v1.auth.schemas import LoginSchema
from billreminder.common.pagination import Pagination, PaginatedList, create_paginated_list_schema, PaginationSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class TestPagination(TestCase):
    def test_properties(self):
        TestData = namedtuple('TestData', ['has_next', 'page', 'total', 'items'])
        data = TestData(has_next=True, page=1, total=12, items=[])

        pagination = Pagination(data)

        self.assertEqual(data.has_next, pagination.has_next)
        self.assertEqual(data.page, pagination.page)
        self.assertEqual(data.total, pagination.total)


class TestPaginatedList(TestCase):
    def test_properties(self):
        TestData = namedtuple('TestData', ['has_next', 'page', 'total', 'items'])
        data = TestData(has_next=True, page=1, total=12, items=[1, 2, 3, 4])
        paginated_list = PaginatedList(data)

        self.assertEqual(data.has_next, paginated_list.pagination.has_next)
        self.assertEqual(data.page, paginated_list.pagination.page)
        self.assertEqual(data.total, paginated_list.pagination.total)
        self.assertEqual(data.items, paginated_list.items)


class TestPaginationSchema(TestCase):
    def test_dump(self):
        data = {
            'page': 1,
            'has_next': False,
            'total': 14
        }

        schema = PaginationSchema()
        dumped, errors = schema.dump(data)

        self.assertEqual(len(errors.keys()), 0)
        self.assertEqual(dumped['page'], data['page'])
        self.assertEqual(dumped['has_next'], data['has_next'])
        self.assertEqual(dumped['total_items'], data['total'])

    def test_paginated_list_dump(self):
        pagination = {
            'page': 1,
            'has_next': False,
            'total': 14
        }

        items = [
            {
                'email': 'test0@mail.com',
                'password': 'abcd1234'
            },
            {
                'email': 'test1@mail.com',
                'password': 'abcd1234'
            }
        ]

        data = {
            'pagination': pagination,
            'items': items
        }

        nested_schema = LoginSchema()
        schema = create_paginated_list_schema(nested_schema)

        dumped, errors = schema.dump(data)

        self.assertEqual(len(errors.keys()), 0)
        self.assertEqual(dumped['pagination']['page'], pagination['page'])
        self.assertEqual(dumped['pagination']['has_next'], pagination['has_next'])
        self.assertEqual(dumped['pagination']['total_items'], pagination['total'])
        self.assertEqual(len(data['items']), len(items))
        self.assertEqual(dumped['items'][0]['email'], items[0]['email'])
        self.assertEqual(dumped['items'][0]['password'], items[0]['password'])
        self.assertEqual(dumped['items'][1]['email'], items[1]['email'])
        self.assertEqual(dumped['items'][1]['password'], items[1]['password'])
