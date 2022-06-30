from rest_framework import serializers

from ..models import Event
from ...attendees.models import AttendeesGroup

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        attenddees_group = AttendeesGroup.objects.get(pk=ret['attendees_group'])
        
        return {
            'id': ret['id'],
            'name': ret['name'],
            'group_users': attenddees_group.name,
            'group_users_id': attenddees_group.id,
            'place': ret['place'],
            'date': ret['finish_date'],
            'not_hours': ret['count_hours'],
            "count_trade_show_hours": ret['count_trade_show_hours'],
        }