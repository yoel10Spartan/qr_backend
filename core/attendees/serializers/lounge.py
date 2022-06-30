from rest_framework import serializers

from ..models import Lounge

class LoungeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lounge
        fields = '__all__'
        
class GETLoungeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lounge
        fields = ['id', 'name', 'aforo_current', 'aforo']