from unittest import TestCase

from billreminder.app import create_app
from billreminder.extensions import db
from billreminder.settings import TestConfig


class BaseTest(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.db = db

    def create_app(self):
        return create_app(config_object=TestConfig)

    def setUp(self):
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.db.get_engine(self.app).dispose()
