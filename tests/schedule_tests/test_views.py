from datetime import date

from django.test.utils import override_settings

from schedule.models import Calendar
from tests.base import TestBase


@override_settings(ROOT_URLCONF='tests.urls')
class TestScheduleView(TestBase):

    def test_schedule(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/schedule/')
        print(response)
        self.assertTemplateUsed(response, template_name='schedule/schedule_list.html')

    def test_not_logged_in(self):
        response = self.client.get('/schedule/change/2018/12/19/7/')
        self.assertRedirects(response, '/admin/login/?next=/schedule/change/2018/12/19/7/')

    def test_admin_logged_in(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/schedule/change/2018/12/19/7/')
        self.assertRedirects(response, '/schedule/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19), is_closed=True).exists())

    def test_user_logged_in(self):
        self.assertTrue(self.client.login(**self.simple_creds))
        response = self.client.get('/schedule/change/2018/12/19/7/')
        self.assertRedirects(response, '/schedule/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19), is_closed=False, out=True).exists())

    def test_user_logged_in_change(self):
        self.assertTrue(self.client.login(**self.simple_creds))
        self.client.get('/schedule/change/2018/12/19/7/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        response = self.client.get('/schedule/change/2018/12/19/7/')
        self.assertRedirects(response, '/schedule/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19), is_closed=False, out=False).exists())

    def test_admin_logged_in_change(self):
        self.assertTrue(self.client.login(**self.credentials))
        self.client.get('/schedule/change/2018/12/19/7/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        response = self.client.get('/schedule/change/2018/12/19/7/')
        self.assertRedirects(response, '/schedule/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19), is_closed=False).exists())

    def test_user_logged_in_change_twice(self):
        self.assertTrue(self.client.login(**self.simple_creds))
        self.client.get('/schedule/change/2018/12/19/7/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        self.client.get('/schedule/change/2018/12/19/7/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        response = self.client.get('/schedule/change/2018/12/19/7/')
        self.assertRedirects(response, '/schedule/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19), is_closed=False, out=True).exists())

    def test_admin_logged_in_change_twice(self):
        self.assertTrue(self.client.login(**self.credentials))
        self.client.get('/schedule/change/2018/12/19/7/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        self.client.get('/schedule/change/2018/12/19/7/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        response = self.client.get('/schedule/change/2018/12/19/7/')
        self.assertRedirects(response, '/schedule/')
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19)).exists())
        self.assertTrue(Calendar.objects.filter(calendar_day=date(2018, 12, 19), is_closed=True).exists())
