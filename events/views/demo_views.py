from django.views.generic.dates import ArchiveIndexView, MonthArchiveView
from django.template import RequestContext, Template
from django.core import serializers
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from events.models import Venue, Event, MyClubUser
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Generic Date View

class ArchiveIndexViewDemo(ArchiveIndexView):
    model=Event
    date_field="event_date"
    allow_future = True

class MonthArchiveViewDemo(MonthArchiveView):
    queryset = Event.events.all()
    date_field="event_date"
    context_object_name = 'event_list'
    allow_future = True
    month_format = '%m'

# ListView-DetailView-finis
class EventListView(ListView):
    model = Event
    context_object_name = 'all_events'
class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'
class EventCreateView(CreateView):
    model = Event    
    fields = ['name', 'event_date', 'description']
    success_url = reverse_lazy('show-events')

class EventUpdateView(UpdateView):
    model = Event
    fields = ['name', 'event_date', 'description']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('show-events')
class EventDeleteView(DeleteView):
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('show-events')



def gen_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="bart.txt"'
    lines = [
    "I will not expose the ignorance of the faculty.\n",
    "I will not conduct my own fire drills.\n",
    "I will not prescribe medication.\n",
    ]
    response.writelines(lines)
    return response
def gen_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'
    writer = csv.writer(response)
    venues = Venue.venues.all()
    writer.writerow(['Venue Name', 'Address', 'Phone', 'Email'])
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.email_address])
    return response
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

def template_demo(request):
        empty_list = []
        color_list = ['red', 'green', 'blue', 'yellow']
        somevar = 5
        anothervar = 21
        today = datetime.now()
        past = datetime(1985, 11, 5)
        future = datetime(2035, 11, 5)
        best_bands = [
            {'name': 'The Angels', 'country': 'Australia'},
            {'name': 'AC/DC', 'country': 'Australia'},
            {'name': 'Nirvana', 'country': 'USA'},
            {'name': 'The Offspring', 'country': 'USA'},
            {'name': 'Iron Maiden', 'country': 'UK'},
            {'name': 'Rammstein', 'country': 'Germany'},
        ]
        aussie_bands = ['Australia', ['The Angels', 'AC/DC', 'The Living End']]
        venues_js = serializers.serialize('json', Venue.venues.all())
        return render(request, 'events/template_demo.html',
        {
            'somevar': somevar,
            'anothervar': anothervar,
            'empty_list': empty_list,
            'color_list': color_list,
            'best_bands': best_bands,
            'today': today,
            'past': past,
            'future': future,
            'aussie_bands': aussie_bands,
            'venues': venues_js,
        })

# RequestContext example

def context_demo(request):

#    template = Template('{{ user }}<br>{{ perms }}<br>{{ request}}<br>{{ messages }}')
#    template = Template('{{ LANGUAGE_CODE }}<br>{{ LANGUAGE_BIDI }}')
   template = Template('{{ foo }}<br>{{ bar }}<br>{{ baz }}')
   
   con = RequestContext(request, processors=[my_processor])
   
   return HttpResponse(template.render(con))

# Custom Context Processor example
def my_processor(request):
    return {
    'foo': 'foo',
    'bar': 'bar',
    'baz': 'baz',
    }
class TemplateViewDemo(TemplateView):
    template_name = "events/cbv_demo.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Testing The TemplateView CBV"
        return context