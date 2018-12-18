from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^schedule/', include('schedule.urls')),
    url(r'', include('cms.urls')),
]
