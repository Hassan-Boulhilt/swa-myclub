from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime


# Template Filers

register = template.Library()
@register.filter(name='reverse')
@stringfilter
def reverse(value):
    return value[::-1]

# Template Tags
# 1- Simple Tag

@register.simple_tag
def create_date(date_val):
    return "This content was created on %s" % date_val.strftime('%A %B %d, %Y')

# 2- Complex Tag "inclusion"
@register.inclusion_tag('events/announcements.html')
def announcements():
    announcements = [
         {
             'date': '6-10-2020',
             'announcement': "Club Registrations Open"
         },
         {
             'date': '6-15-2020',
             'announcement': "Joe Smith Elected New Club President"
         }
    ]
    return {'announcements': announcements}


