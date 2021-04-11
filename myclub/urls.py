"""myclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from events import urls
from django.contrib import admin
from events.admin import admin_site
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import contact
from django.views.generic.base import TemplateView
from events.views import TemplateViewDemo
from django.views.generic.base import RedirectView
# admin.site.site_header = "Swa-Club Administration"
# admin.site.site_title  = "Swa-Club Site Admin"
# admin.site.index_title = "Swa-Club Site Admin Home"


urlpatterns = [
    # path('cbvdemo/', TemplateView.as_view(template_name='events/cbv_demo.html')),
    path('home/', RedirectView.as_view(url='/', permanent=True)),
    path('cbvdemo/', TemplateViewDemo.as_view()),
    path('admin/', admin.site.urls), 
    path('eventsadmin/',admin_site.urls), 
    # path('contact/', contact.contact, name='contact'),
    path('contact/', contact.ContactUs.as_view(), name='contact'),
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', include('events.urls')),
]
