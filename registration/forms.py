from django.shortcuts import reverse
from django.views import generic

from registration.models import Registration


class CreateRegistration(generic.CreateView):
    model = Registration
    fields = '__all__'

    def get_success_url(self):
        return reverse('')


class RegistrationList(generic.ListView):
    model = Registration
    queryset = Registration.objects.all()
    context_object_name = 'form'
