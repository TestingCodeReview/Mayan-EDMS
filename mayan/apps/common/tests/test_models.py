from __future__ import unicode_literals

from common.tests import BaseTestCase
from user_management.tests.mixins import UserTestMixin


class UserLocaleProfileTestCase(UserTestMixin, BaseTestCase):
    def test_natural_keys(self):
        self._create_user()
        self._test_database_conversion('auth', 'common')
