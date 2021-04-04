from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from .models import Venue, MyClubUser, Event
from events.forms import VenueForm

class EventsAdmin(AdminSite):
    site_header = "Swa-Club Administration"
    site_title  = "Swa-Club Site Admin"
    index_title = "Swa-Club Site Admin Home"
admin_site = EventsAdmin(name='eventsadmin')
@admin.register(Venue,site=admin_site)
class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
    list_display =('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name','address')

@admin.register(Event, site=admin_site)
class EventAdmin(admin.ModelAdmin):
    # fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    list_display = ('name', 'event_date','venue' )
    list_filter = ('event_date','venue')
    ordering = ('-event_date',)
    fieldsets = (
        ('Required Information', {
            "description": "These fields are required for each event.",
            "fields": (('name', 'venue'), 'event_date')
                
            
        }),
        ('Optional Information', {
            "classes": ("collapse",),
            "fields": ('description', 'manager')
                
            
        }),
    )
    

# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event)
admin_site.register(User)
admin_site.register(Group)


