from django.urls import path, re_path
from . import views
from .views import ListViewDemo, DetailViewDemo
urlpatterns=[

    path('',views.index, name="index"),
    path('condemo/', views.context_demo, name='condemo'),
    path('template_demo/', views.template_demo, name='template_demo'),
    # path('<int:year>/<str:month>/', views.index, name="index"),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>0?[1-9]|1[0-2])/', views.index, name='index'),
    # path('events/', views.all_events, name='event_list'),
    path('events/',ListViewDemo.as_view(),name="show_events"),
    path('event/<int:pk>/',DetailViewDemo.as_view(),name="event-detail"),
    path('add_venue/', views.add_venue, name='add-venue'),
    path('genpdf/', views.gen_pdf, name='generate-pdf-file'),
    path('getsubs/', views.list_subscribers, name='list-subscribers'),
]