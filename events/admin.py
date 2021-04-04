from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from .models import Venue, MyClubUser, Event
from events.forms import VenueForm

# Model admin option TabularInline "ManyToMany" relation
class AttendeeInline(admin.TabularInline):

    model = Event.attendees.through

    verbose_name = 'Attendee'

    verbose_name_plural = 'Attendees'
class EventsAdmin(AdminSite):
    site_header = "Swa-Club Administration"
    site_title  = "Swa-Club Site Admin"
    index_title = "Swa-Club Site Admin Home"
admin_site = EventsAdmin(name='eventsadmin')

#  Model admin option StackedInline "simple model"
class EventInline(admin.StackedInline):

    model = Event

    fields = ('name', 'event_date')

    extra = 1
@admin.register(Venue,site=admin_site)
class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
    list_display =('name', 'address', 'phone')
    # list_display_links = ('name', 'address')
    # list_editable = ('phone',)
    list_editable = list_display
    list_display_links = None
    ordering = ('name',)
    search_fields = ('name','address')
    
    inlines = [
        EventInline,
        ]

@admin.register(Event, site=admin_site)
class EventAdmin(admin.ModelAdmin):
    # fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    list_display = ('name', 'event_date','venue' )
    list_filter = ('event_date','venue')
    ordering = ('-event_date',)
    save_as = True
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
    inlines = [
        AttendeeInline,
        ]
    

# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event)
admin_site.register(User)
admin_site.register(Group)


