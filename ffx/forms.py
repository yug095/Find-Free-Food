from django import forms
from models import Profile, Event
from django.contrib.auth.models import User
from location_field.forms.plain import PlainLocationField


class RegistrationUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class RegistrationProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('major', 'address', 'phone')

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'title', 'event_date', 'event_endtime', 'address', 'event_type',
            'description', 'location_text', 'capacity', 'requires_major', 'image_url',
            'map_marker'
        )
