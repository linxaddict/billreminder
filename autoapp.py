from flask.helpers import get_debug_flag

from billreminder.app import create_app
from billreminder.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

if __name__ == '__main__':
    app.run()
