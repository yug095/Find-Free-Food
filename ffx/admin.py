from django.contrib import admin

from .models import Event, EventType, Registration, Profile

admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Registration)
admin.site.register(Profile)