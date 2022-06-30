from rest_framework import serializers
from ..db import Attendee, AttendeesGroup

class AttendeeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendeesGroup
        fields = '__all__'
        
class GETAttendeeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendeesGroup
        fields = ['id', 'name']
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        id_attendee_group = ret['id']
        ret['total'] = AttendeesGroup.objects.get(pk=id_attendee_group).attendees.count()
        return ret