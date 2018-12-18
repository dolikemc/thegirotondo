from datetime import date
from unittest import mock

from schedule.models import Consideration, Calendar
from tests.base import TestBase


class TestCalendar(TestBase):
    def setUp(self):
        super(TestCalendar, self).setUp()
        for i in range(1, 51):
            Consideration.objects.create(day=i)

    def test_str(self):
        consideration = Consideration.objects.get(id=1)
        self.assertEqual('1', str(consideration))

    @mock.patch('schedule.models.date')
    def test_is_monday(self, mock_date):
        mock_date.today.return_value = date(2018, 12, 17)
        consideration = Consideration.objects.get(id=14)
        self.assertTrue(consideration.is_monday)

    @mock.patch('schedule.models.date')
    def test_is_weekend(self, mock_date):
        mock_date.today.return_value = date(2018, 12, 17)
        consideration = Consideration.objects.get(id=13)
        self.assertFalse(consideration.is_monday)
        self.assertTrue(consideration.is_weekend)

    @mock.patch('schedule.models.date')
    def test_is_sunday(self, mock_date):
        mock_date.today.return_value = date(2018, 12, 17)
        consideration = Consideration.objects.get(id=13)
        self.assertTrue(consideration.is_sunday)

    @mock.patch('schedule.models.date')
    def test_date(self, mock_date):
        mock_date.today.return_value = date(2018, 12, 17)
        consideration = Consideration.objects.get(id=14)
        self.assertEqual(date(2018, 12, 17), consideration.date)

    @mock.patch('schedule.models.date')
    def test_first_monday_on_monday(self, mock_date):
        mock_date.today.return_value = date(2018, 12, 17)
        self.assertEqual(7, Consideration.get_first_monday())

        mock_date.today.return_value = date(2018, 12, 24)
        self.assertEqual(7, Consideration.get_first_monday())

    @mock.patch('schedule.models.date')
    def test_first_monday_on_tuesday(self, mock_date):
        mock_date.today.return_value = date(2018, 12, 18)
        self.assertEqual(6, Consideration.get_first_monday())

    @mock.patch('schedule.models.date')
    def test_first_monday_on_sunday(self, mock_date):
        mock_date.today.return_value = date(2018, 12, 30)
        self.assertEqual(1, Consideration.get_first_monday())

    @mock.patch('schedule.models.date')
    def test_is_closed(self, mock_date):
        mock_date.today.return_value = date(2018, 12, 30)
        consideration = Consideration.objects.get(id=14)
        self.assertFalse(consideration.is_closed)

    @mock.patch('schedule.models.date')
    def test_no_outs(self, mock_date):
        mock_date.today.return_value = date(2018, 12, 30)
        consideration = Consideration.objects.get(id=14)
        self.assertEqual(0, len(consideration.exists_out))

    @mock.patch('schedule.models.date')
    def test_with_outs(self, mock_date):
        mock_date.today.return_value = date(2018, 12, 30)
        consideration = Consideration.objects.get(id=14)
        Calendar.objects.create(user_id=self.admin.id, calendar_day=mock_date.today.return_value, out=True)
        self.assertEqual(1, len(consideration.exists_out))
        self.assertEqual(1, consideration.exists_out[0].id)
