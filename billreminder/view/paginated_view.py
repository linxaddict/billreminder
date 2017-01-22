from flask_restful import Resource

from billreminder.model.schemas import PaginatedListSchema

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class PaginatedView(Resource):
    QUERY_ARG_PAGE = 'page'
    DEFAULT_PAGE = 1
    ITEMS_PER_PAGE = 50

    paginated_schema = PaginatedListSchema(strict=True)
