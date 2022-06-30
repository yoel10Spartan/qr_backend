from django.db import models
from django.utils.translation import gettext_lazy as _

class Attendee(models.Model):
    id_qr = models.IntegerField(default=0)
    name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    hours = models.CharField(max_length=255, default=0)

    entrie = models.BooleanField(default=False)
    output = models.BooleanField(default=True)

    entrie_datetime = models.DateTimeField(null=True, blank=True)
    output_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return '{} {}'.format(self.name, self.last_name)