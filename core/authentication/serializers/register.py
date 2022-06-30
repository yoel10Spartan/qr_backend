from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from core.users.serializers import UserSerializer
from core.users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True, required=True
    )

    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'username']

    def create(self, validated_data):
        try:
            user = User.objects.get(username=validated_data['username'])
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)
        return user