from django.db import models

class Operator(models.Model):
    id_user = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.username