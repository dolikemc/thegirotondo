from datetime import time, date, timedelta

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Calendar(models.Model):
    is_closed = models.BooleanField(default=True)
    out = models.BooleanField(default=False)
    out_from = models.TimeField(default=time(hour=7, minute=0, second=0))
    user = models.ForeignKey(to=User)
    calendar_day = models.DateField(db_index=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return "%s %s %d-%d %d:%d" % (
            self.user.first_name, self.user.last_name, self.calendar_day.month, self.calendar_day.day,
            self.out_from.hour,
            self.out_from.minute)


class Consideration(models.Model):
    day = models.PositiveIntegerField()

    def __str__(self):
        return str(self.day)

    @property
    def is_monday(self) -> bool:
        return self.date.weekday() == 0

    @property
    def is_sunday(self) -> bool:
        return self.date.weekday() == 6

    @property
    def is_weekend(self) -> bool:
        return self.date.weekday() >= 5

    @property
    def date(self) -> date:
        return date.today() + timedelta(days=self.day - 14)

    @property
    def exists_out(self):  # -> List[User]
        user = []
        for cal in Calendar.objects.filter(calendar_day__exact=self.date, out=True):
            user.append(cal.user)
        return user

    @staticmethod
    def get_first_monday() -> int:
        return 7 - (date.today() + timedelta(days=- 14)).weekday()

    @property
    def is_closed(self) -> bool:
        return Calendar.objects.filter(calendar_day__exact=self.date, is_closed=True).exists()
