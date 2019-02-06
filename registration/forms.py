from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views import generic

from registration.models import Registration


class CreateRegistration(generic.CreateView):
    model = Registration
    fields = '__all__'

    def get_success_url(self):
        return reverse('')


class RegistrationList(LoginRequiredMixin, generic.ListView):
    model = Registration
    queryset = Registration.objects.filter(birth_date__gt=datetime(2013, 1, 1)).order_by('-published')
    context_object_name = 'form'
