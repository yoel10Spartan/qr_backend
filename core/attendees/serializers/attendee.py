from rest_framework import serializers
from ..db import Attendee, Lounge
from .lounge import GETLoungeSerializer
        
class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'
        
class AttendeeWithLoungeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attendee
        fields = ['id', 'id_qr', 'name']
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        id = ret['id']
        ret['lounge'] = Lounge.objects.filter(attendees__id=id).first().name
        return ret
    
class GETGraphicAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = [
            'id', 
            'id_qr', 
            'name', 
            'lastname', 
            'hours', 
            'entrie', 
            'output',
        ]
        
class GETAttendeeLoungeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = [
            'id', 
            'id_qr', 
            'name',
            'last_name',
        ]
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = ' '.join([ret['name'], ret['last_name']])
        del ret['last_name']
        return ret
        