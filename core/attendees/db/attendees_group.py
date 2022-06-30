from django.db import models

from .attendee import Attendee
from .lounge import Lounge

class AttendeesGroup(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='attendees_list')
    
    lounges = models.ManyToManyField(Lounge, blank=True)
    
    attendees = models.ManyToManyField(Attendee, blank=True)
    
    def __str__(self) -> str:
        return self.name