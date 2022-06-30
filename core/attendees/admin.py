from django.contrib import admin
from .db import Attendee, AttendeesGroup, Lounge

admin.site.register(Attendee)
admin.site.register(AttendeesGroup)
admin.site.register(Lounge)