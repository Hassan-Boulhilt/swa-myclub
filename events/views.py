from django.http.response import HttpResponse
from django.shortcuts import render
from datetime import date
import calendar
from calendar import HTMLCalendar
from .models import Event 


def index(request, month=date.today().month, year=date.today().year):
    # t = date.today()
    # month = date.strftime(t, '%b')
    # year = t.year

    month = int(month)
    year = int(year)
    if year < 2000 or year > 2099:
        year = date.today().year
    month_name = calendar.month_name[month]
    cal = HTMLCalendar().formatmonth(year, month)
    title = f"MyClub Event - {month_name}, {year}"
    # return HttpResponse(f'<h1>{title}{cal}</h1>')
    return render(request, 'events/calendar_base.html', {'title':title, 'cal':cal})
def all_events(request):
    event_list = Event.objects.all()
    return render(request, 'events/event_list.html',{'event_list':event_list})