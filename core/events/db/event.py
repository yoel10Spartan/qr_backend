from django.db import models
from django.utils.translation import gettext_lazy as _

from core.attendees.db import AttendeesGroup
from core.users.models import User
from core.operators.models import Operator

class Event(models.Model):
    
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    start_date = models.DateField()
    finish_date = models.DateField()
    total_hours = models.IntegerField()
    
    count_hours = models.BooleanField(default=True)
    count_trade_show_hours = models.BooleanField(default=False)
    
    aforo = models.IntegerField(null=True, blank=True)
    
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    attendees_group = models.ForeignKey(AttendeesGroup, on_delete=models.SET_NULL, null=True)
    
    operators = models.ManyToManyField(Operator, blank=True)
    
    def __str__(self) -> str:
        return self.name