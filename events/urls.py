from django.urls import path, re_path
from . import views
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView
from .views import ArchiveIndexViewDemo, MonthArchiveViewDemo
# from django.views.generic.dates import ArchiveIndexView
# from .models import Event


urlpatterns=[

    path('', views.index, name="index"),
    # path('eventarchive/', ArchiveIndexView.as_view(model=Event, date_field="event_date")),
    path('eventarchive/', ArchiveIndexViewDemo.as_view(), name='index-event'),
    path('<int:year>/<int:month>/', MonthArchiveViewDemo.as_view(), name='event-montharchive'),
    path('condemo/', views.context_demo, name='condemo'),
    path('template_demo/', views.template_demo, name='template-demo'),
    # path('<int:year>/<str:month>/', views.index, name="index"),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>0?[1-9]|1[0-2])/', views.index, name='index'),
    # path('events/', views.all_events, name='event_list'),
    path('events/', EventListView.as_view(), name="show-events"),
    path('event/add/', EventCreateView.as_view(), name='add-event'),
    path('event/<int:pk>/', EventDetailView.as_view(), name="event-detail"),
    path('event/update/<int:pk>/', EventUpdateView.as_view(), name='event-update'),
    path('event/delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),
    path('add_venue/', views.add_venue, name='add-venue'),
    path('genpdf/', views.gen_pdf, name='generate-pdf-file'),
    path('getsubs/', views.list_subscribers, name='list-subscribers'),
]