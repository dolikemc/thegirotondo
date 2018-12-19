from django.conf.urls import *

from registration.forms import RegistrationList, CreateRegistration

app_name = 'calendar'

urlpatterns = [
    url(r'^list/$', RegistrationList.as_view()),
    url(r'^$', CreateRegistration.as_view()),
]
