from rest_framework import serializers
from django.contrib.auth import authenticate

from core.users.models import User
  
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True, required=True
    )
 
    class Meta(object):
        model = User
        fields = ('id', 'name', 'username', 'is_staff', 'is_operator', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
class ReturnUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'name', 'username', 'is_staff', 'is_operator')