from rest_framework import serializers

from ..db import Operator
from ...attendees.db import Lounge

class OperatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        lounge = Lounge.objects.filter(operators__id = ret['id'])
        if not lounge.exists():
            return ret
        
        ret['lounge'] = lounge.first().name
        
        return ret 
    
class GETDataOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = [
            'id', 
            'id_user',
            'name',
            'username',
        ]