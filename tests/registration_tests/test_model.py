from datetime import date, timedelta

from django.test.utils import skipIf

from registration.models import Registration
from tests.base import TestBase


class TestRegistration(TestBase):
    def setUp(self):
        super(TestRegistration, self).setUp()
        age = date.today() - timedelta(days=1.5 * 356)
        self.registration = Registration.objects.create(child_pre_name='Hans', child_name='Kleingeld',
                                                        email='Hans@Kleinkind.com',
                                                        start=date.today(), birth_date=age, sex='M',
                                                        father_name='x',
                                                        father_profession='x',
                                                        father_mobile='x',
                                                        father_email='Hans@Kleinkind.com',
                                                        mother_name='y',
                                                        mother_profession='y',
                                                        mother_mobile='y',
                                                        mother_email='Hans@Kleinkind.com',
                                                        street='xy',
                                                        number='2a',
                                                        zip='A34',
                                                        city='München',
                                                        fon='234',
                                                        urgency='B',
                                                        privacy=True,
                                                        data_protection=True,
                                                        ip_address='1.1.1.0')

    def test_str_registration(self):
        self.assertEqual('1 Hans Kleingeld: Hans@Kleinkind.com', str(self.registration))

    def test_age(self):
        self.assertEqual(1, self.registration.age)

    @skipIf(True, 'not yet implemented')
    def test_url(self):
        pass
