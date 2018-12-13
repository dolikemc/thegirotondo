from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from schedule.forms import CreateOutTime, ShowCalendar


@apphook_pool.register  # register the application
class CalendarApphook(CMSApp):
    app_name = "calendar"
    name = _("Calendar Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^add/$', CreateOutTime.as_view()),
            url(r'^$', ShowCalendar.as_view()),
        ]
