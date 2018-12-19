from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from schedule.models import Consideration


class ShowCalendar(LoginRequiredMixin, generic.ListView):
    model = Consideration
    login_url = '/admin/login/'
    context_object_name = 'form'
    template_name = 'schedule/schedule_list.html'

    def get_queryset(self):
        return Consideration.objects.filter(day__gte=Consideration.get_first_monday(),
                                            day__lt=Consideration.get_first_monday() + 56).order_by('day')
