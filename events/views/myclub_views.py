from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.paginator import Paginator
from datetime import date
import calendar
from calendar import HTMLCalendar
from events.models import Event, Venue, MyClubUser
from events.forms import VenueForm


# Show calaendar in home page 
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
    announcements = [
        {
            'date': '20-03-2021',
            'announcement': "Club Registrations Open"
        },
         {
            'date': '13-04-2021',
            'announcement': "Joe Smith Elected New Club President"
        }
    ]
    title = f"MyClub Event - {month_name}, {year}"
    # return HttpResponse(f'<h1>{title}{cal}</h1>')
    return render(request, 'events/calendar_base.html', {'title':title, 'cal':cal,'announcements':announcements})

# Display all events
def all_events(request):
    event_list = Event.objects.all()
    return render(request, 'events/event_list.html',{'event_list':event_list})

# Add venue to event model 

def add_venue(request):
     submitted = False
     if request.method == 'POST':
         form = VenueForm(request.POST)
         if form.is_valid():
             form.save()
             return HttpResponseRedirect('/add_venue/?submitted=True')
     else:
         form = VenueForm()
         if 'submitted' in request.GET:
             submitted = True
     return render(request, 
         'events/add_venue.html', 
         {'form': form, 'submitted': submitted}
         )

def list_subscribers(request):
     p = Paginator(MyClubUser.objects.all(), 2)
     page = request.GET.get('page')
     subscribers = p.get_page(page)
     return render(request, 'events/subscribers.html', {'subscribers': subscribers})