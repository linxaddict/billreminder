from enum import Enum

from billreminder.http_status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, \
    HTTP_404_NOT_FOUND

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class ApiErrors(Enum):
    NO_INPUT_DATA = {'error': 'No input data provided'}, HTTP_400_BAD_REQUEST
    EMAIL_ALREADY_TAKEN = {'error': 'This e-mail address is already taken'}, HTTP_409_CONFLICT
    INVALID_EMAIL_OR_PASSWORD = {'error': 'Invalid e-mail address or password'}, HTTP_401_UNAUTHORIZED
    NO_RESULT_FOUND = {'error': 'No result found'}, HTTP_404_NOT_FOUND
    MULTIPLE_RESULTS_FOUND = {'error': 'Multiple results found'}, HTTP_400_BAD_REQUEST
    ACCESS_DENIED = {'error': 'Access denied'}, HTTP_403_FORBIDDEN
    BILL_NOT_FOUND = {'error': 'Bill not found'}, HTTP_404_NOT_FOUND
    UNAUTHORIZED = {'error': 'Unauthorized'}, HTTP_401_UNAUTHORIZED
    BAD_REQUEST = {'error': 'Invalid input data'}, HTTP_400_BAD_REQUEST
    USER_NOT_FOUND = {'error': 'User not found'}, HTTP_404_NOT_FOUND
