from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from datetime import date
import calendar
from calendar import HTMLCalendar
from .models import Event 
from .forms import VenueForm
# PDF import
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# PDF implement 

def gen_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica-Oblique", 14)
    lines = [
    "I will not expose the ignorance of the faculty.",
    "I will not conduct my own fire drills.",
    "I will not prescribe medication.",
    ]
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='bart.pdf')

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