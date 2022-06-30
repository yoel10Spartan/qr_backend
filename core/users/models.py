from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
 
class UserManager(BaseUserManager):
    def _create_user(self, username, name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            name = name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, name, password, is_staff=False, is_superuser=False, **extra_fields):
        return self._create_user(username, name, password, False, False, **extra_fields)

    def create_superuser(self, username, name, password, is_staff=True, is_superuser=True, **extra_fields):
        return self._create_user(username, name, password, True, True, **extra_fields)
 
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_operator = models.BooleanField(default=False)
 
    objects = UserManager()
    
    def get_full_name(self):
        return '{} {}'.format(self.name, self.last_name)
    
    class Meta:
        db_table = 'auth_user'
 
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']