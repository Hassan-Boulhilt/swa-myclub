from django.db import models
from django.contrib.auth.models import User

# subclass models.Manager to build custom model that inherits all its methods

class EventManager(models.Manager):
    def event_type_count(self, event_type):
        return self.filter(name__icontains=event_type).count()
# subclass models.Manager to build custom model and override one of its methods "get_queryset" method
class VenueManager(models.Manager):
     def get_queryset(self):
         return super(VenueManager, self).get_queryset().filter(zip_code='00000')

class Venue(models.Model):
    name= models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip/Post Code', max_length=12)
    phone = models.CharField('Contact Phone', max_length=20, blank=True)
    web = models.URLField('Web Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)
    venues = models.Manager()
    local_venues = VenueManager()

    def __str__(self):
        return self.name
class MyClubUser(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=30)
    volunteer = models.BooleanField(default=False)

    def __str__(self):
        # return f"{self.first_name} {self.last_name}"
        return ''

MEMBER_CHOICES = [
    ('A', 'Adult'),
    
    ('J', 'Junior'),
    
    ('C', 'Concession'),
     ]
class Subscriber(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL)       
    member_level = models.CharField(max_length=1, choices=MEMBER_CHOICES, default='A')

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    events = EventManager()
    attendees = models.ManyToManyField(MyClubUser, blank=True)

    # add a custom method to model Event
    def event_timing(self, date):
         if self.event_date > date:
             return "Event is after this date"
         elif self.event_date == date:
             return "Event is on the same day"
         else:
             return "Event is before this date"
    # override a method in Event model "name_slug" and use decorator that allows access method directly
    @property
    def name_slug(self):
         return self.name.lower().replace(' ','-')

    # override save method 
    def save(self, *args, **kwargs):
         self.manager = User.objects.get(username='admin') # User 'admin' must exist
         super(Event, self).save(*args, **kwargs)


    def __str__(self):
        return self.name



    
 

