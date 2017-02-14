from flask_testing import TestCase

from billreminder.extensions import db

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class BaseTest(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.db = db

    def create_app(self):
        # return create_app(config_object=TestConfig)
        from autoapp import app
        return app

    @property
    def json_content_type(self):
        return 'application/json'

    def setUp(self):
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.db.get_engine(self.app).dispose()
