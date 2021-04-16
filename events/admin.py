from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from .models import Venue, MyClubUser, Event, Subscriber
from events.forms import VenueForm
from django.http import HttpResponse
import csv
from django import forms
from ckeditor.widgets import CKEditorWidget


# Model MyClubUser option stackinline

class MyClubUserInline(admin.StackedInline):
    model =MyClubUser
    can_delete = False
    verbose_name = "Address and Phone"
    verbose_name_plural = "Additional Info"

class MyClubUserAdmin(UserAdmin):
    inlines = (MyClubUserInline,)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'member_level')
    list_filter = ('member_level',)




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
# @admin.register(Venue,site=admin_site)
@admin.register(Venue)
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

    # Override get_list_display methods's ModelAdmin
    def get_list_display(self, request):
        return ('name', 'address', 'phone', 'web')
# Bulk actions that modify one or more records 
def set_manager(modeladmin, request, queryset):
    queryset.update(manager=request.user)
set_manager.short_description = "Manage selected events"

# Exporting data from database tables and saving it in a comma-delimited file

def venue_csv(modeladmin, request, queryset):

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="venue_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'event_date', 'venue', 'description'])

    for record in queryset:
        rec_list = []
        rec_list.append(record.name)
        rec_list.append(record.event_date.strftime("%m/%d/%Y,%H:%M"))
        rec_list.append(record.venue.name)
        rec_list.append(record.description)
        writer.writerow(rec_list)
    
    return response
venue_csv.short_description = "Export Selected Venues to CSV"

class EventAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Event
        fields = '__all__'
    
# @admin.register(Event, site=admin_site)
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    form = EventAdminForm
    list_display = ('name', 'event_date', 'venue', 'manager')
    list_filter = ('event_date','venue')
    ordering = ('-event_date',)
    save_as = True
    actions = [set_manager, venue_csv]
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
    


admin.site.register(MyClubUser)
admin.site.unregister(User)
admin.site.register(User, MyClubUserAdmin)
# admin_site.register(Group)




