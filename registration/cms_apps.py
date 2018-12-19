from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from registration.forms import CreateRegistration, RegistrationList
from registration.urls import urlpatterns


@apphook_pool.register  # register the application
class RegistrationApphook(CMSApp):
    app_name = "registration"
    name = _("Registration Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return urlpatterns
