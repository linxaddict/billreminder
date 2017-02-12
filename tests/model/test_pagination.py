from collections import namedtuple
from unittest import TestCase

from billreminder.model.pagination import Pagination, PaginatedList

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

TestData = namedtuple('TestData', ['has_next', 'page', 'total', 'items'])


class TestPagination(TestCase):
    def test_properties(self):
        data = TestData(has_next=True, page=1, total=12, items=[])

        pagination = Pagination(data)

        self.assertEqual(data.has_next, pagination.has_next)
        self.assertEqual(data.page, pagination.page)
        self.assertEqual(data.total, pagination.total)


class TestPaginatedList(TestCase):
    def test_properties(self):
        data = TestData(has_next=True, page=1, total=12, items=[1, 2, 3, 4])
        paginated_list = PaginatedList(data)

        self.assertEqual(data.has_next, paginated_list.pagination.has_next)
        self.assertEqual(data.page, paginated_list.pagination.page)
        self.assertEqual(data.total, paginated_list.pagination.total)
        self.assertEqual(data.items, paginated_list.items)
