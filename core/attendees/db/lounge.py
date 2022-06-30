from django.db import models

from .attendee import Attendee
from core.operators.db import Operator

class Lounge(models.Model):
    name = models.CharField(max_length=255)
    aforo = models.IntegerField(null=True, blank=True, default=0)
    aforo_current = models.IntegerField(null=True, blank=True, default=0)
    afoto_total = models.IntegerField(null=True, blank=True, default=0)
    
    attendees = models.ManyToManyField(Attendee, blank=True)
    
    operators = models.ManyToManyField(Operator, blank=True)
    
    def __str__(self) -> str:
        return self.name