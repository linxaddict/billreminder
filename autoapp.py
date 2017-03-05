import os

from flask.helpers import get_debug_flag

from billreminder.app import create_app
from billreminder.settings import DevConfig, ProdConfig, TestConfig


def get_test_flag(default=None):
    val = os.environ.get('FLASK_TEST')
    if not val:
        return default
    return val not in ('0', 'false', 'no')

if get_test_flag():
    CONFIG = TestConfig
else:
    CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
