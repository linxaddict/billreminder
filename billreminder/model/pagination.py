__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


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
