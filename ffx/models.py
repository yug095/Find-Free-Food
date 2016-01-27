from datetime import datetime
import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from location_field.models.plain import PlainLocationField


class EventType(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField('brief description of the event type')

    def __unicode__(self):
        return self.name.encode('utf-8')


class Event(models.Model):
    event_id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    event_type = models.ManyToManyField(EventType, blank=True)
    description = models.TextField('description of the event')
    event_date = models.DateTimeField()
    event_endtime = models.TimeField(blank=True, null=True, help_text='Time event ends, leave blank for no set duration.')
    created_date = models.DateTimeField(default=datetime.now(),editable=False)
    address = models.CharField('address', max_length=128, default='', help_text='Can be as specific as a street address, or as broad as a city')
    map_marker = PlainLocationField(based_fields=[address], zoom=7, blank=True, help_text='Enter an address in the Address field to center the map on that location')
    location_text = models.TextField('additional location details', max_length=256, blank=True, help_text='Useful extra description of the location, if needed. Ex: in front of the Starbucks, or in Room 415 of Building 3A')
    organizer = models.ForeignKey(User)
    capacity = models.PositiveIntegerField(help_text='Capacity must be positive, or enter 0 for no limit.', default=0)
    public = models.BooleanField(default=True, help_text='If unchecked, event will only be visible to registered users')
    requires_major = models.CharField(max_length=100, help_text='Major required for attendance',blank=True)
    image_url = models.ImageField(upload_to='events',blank=True, help_text='Upload an image that will appear with your event in the listing')

    def __unicode__(self):
        return self.title.encode('utf-8')

    def get_event_type(self):
        return ", ".join([e.name for e in self.event_type.all()])

    def get_reg_count(self):
        return Registration.objects.filter(event=self.event_id).count()

    def get_reg_user_ids(self):
        return Registration.objects.filter(event=self.event_id).values_list('user_id', flat=True)

    def latitude(self):
        return self.map_marker.split(',')[0]

    def longitude(self):
        return self.map_marker.split(',')[1]


class Registration(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    reg_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.user.__unicode__() + ' registered for ' + self.event.__unicode__()


# Used to extend properties of the User model, as per recommendation from the authors
class Profile(models.Model):
    user = models.ForeignKey(User)
    major = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s's profile" % self.user
