from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from schedule.urls import urlpatterns


@apphook_pool.register  # register the application
class CalendarApphook(CMSApp):
    app_name = "calendar"
    name = _("Calendar Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return urlpatterns
