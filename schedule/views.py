from datetime import date, time

from django.contrib.auth.views import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from schedule.models import Calendar


@login_required(login_url='/admin/login/')
def change_out_time(request: HttpRequest, year: str, month: str, day: str, hour: str = '7') -> HttpResponse:
    entry_date = date(year=int(year), month=int(month), day=int(day))
    entry = Calendar.objects.filter(user_id=request.user.id, calendar_day=entry_date).first()

    if request.user.is_superuser:
        if entry is None:
            Calendar.objects.create(user_id=request.user.id, calendar_day=entry_date, is_closed=True,
                                    out_from=time(int(hour), minute=0, second=0))
        elif entry.is_closed:
            entry.is_closed = False
            entry.out = False
            entry.save()
        else:
            entry.is_closed = True
            entry.out = False
            entry.save()
        return redirect(to='calendar:show-calendar')

    if entry is None:
        Calendar.objects.create(user_id=request.user.id, calendar_day=entry_date, out=True,
                                out_from=time(int(hour), minute=0, second=0), is_closed=False)
    elif entry.out is True:
        entry.out = False
        entry.save()
    else:
        entry.out = True
        entry.save()
    return redirect(to='calendar:show-calendar')
