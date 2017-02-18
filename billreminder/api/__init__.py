from flask import Blueprint
from billreminder.api.v1 import *
from billreminder.api.v1.auth import *

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

blueprint = Blueprint('api_v1', __name__)
