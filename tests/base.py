from cms.test_utils.testcases import CMSTestCase
from django.contrib.auth.models import User
from django.test.utils import override_settings


@override_settings(ROOT_URLCONF='tests.urls')
class TestBase(CMSTestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username=self.credentials['username'],
                                                   email='a@b.com',
                                                   password=self.credentials['password'])
        self.user = User.objects.create_user(self.simple_creds['username'], 'u@b.com',
                                             self.simple_creds['password'],
                                             **{'is_staff': True})

    @property
    def credentials(self):
        return {'username': 'ad', 'password': 'secret'}

    @property
    def simple_creds(self):
        return {'username': 'us', 'password': 'secret'}
