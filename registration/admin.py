from django.contrib import admin

from registration.models import Registration


class RegistrationAdmin(admin.ModelAdmin):
    model = Registration
    list_display = (
        'id', 'child_pre_name', 'child_name', 'email', 'birth_date', 'published', 'start', 'mother_profession')
    list_filter = ('language', 'sex')


admin.site.register(Registration, RegistrationAdmin)
