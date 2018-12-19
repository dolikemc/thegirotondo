from django.conf.urls import *

from schedule import views
from schedule.forms import ShowCalendar

app_name = 'calendar'

urlpatterns = [
    url(r'^change/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<hour>[0-9]+)/$',
        views.change_out_time, name='change-entry'),
    url(r'^$', ShowCalendar.as_view(), name='show-calendar'),
]
