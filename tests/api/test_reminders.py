from tests.base import BaseTest, ViewTestMixin

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class RemindersViewTest(ViewTestMixin, BaseTest):
    url = '/reminders'

    def test_fetch(self):
        pass
