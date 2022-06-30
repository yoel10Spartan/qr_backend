from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import Lounge
from ..serializers import LoungeSerializer, GETLoungeSerializer
from ...messages.spanish import *

import core.attendees.viewsets
from core.operators.models import Operator

class LoungeManagement:
    model = Lounge
    
    def __init__(self, id) -> None:
        self.id = id
        
    def get_queryset(self):
        return self.model.objects.get(pk=self.id)
    
    def add_lounge(self, attendee):
        lounge = self.get_queryset()
        lounge.attendees.add(attendee)
        lounge.save()
        
    def add_lounge_group(self, id_attendees_group):
        attendee_group_management = core.attendees.viewsets.AttendeeGroupManagement(id_attendees_group)
        attendee_group_management.add_lounge(self.get_queryset())
    
    def add_operator(self, operator):
        lounge = self.get_queryset()
        lounge.operators.add(operator)
        lounge.save()
        
    def remove_operator(self, operator):
        lounge = self.get_queryset()
        lounge.operators.remove(operator)
        lounge.save()
        
    def remove_attendee(self, attendee):
        lounge = self.get_queryset()
        lounge.attendees.remove(attendee)
        lounge.save()
        
    def get_lounge_operator(self, id_operator):
        lounge = Lounge.objects.filter(operators__id=id_operator)
        return lounge
    
    def increase_aforo(self):
        lounge = self.get_queryset()
        lounge.aforo_current += 1
        lounge.save()
        
    def increase_total_aforo(self):
        lounge = self.get_queryset()
        lounge.afoto_total += 1
        lounge.save()
    
    def decrease_aforo(self):
        lounge = self.get_queryset()
        lounge.aforo_current -= 1
        lounge.save()
    
    @classmethod
    def search(cls, **kwargs):
        return cls.model.objects.filter(**kwargs)
    
class LoungeViewSet(viewsets.ModelViewSet):
    serializer_class = LoungeSerializer
    queryset = Lounge.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        id_attendees_group = request.data['attendees_group']
        id_lounge = serializer.data['id']
        
        lounge_management = LoungeManagement(id_lounge)
        lounge_management.add_lounge_group(id_attendees_group)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['GET'], detail=True)
    def get_for_group(self, request, pk):
        queryset = self.filter_queryset(self.get_queryset())
        filter_for_group = queryset.filter(attendeesgroup__id = pk)
        serializer = GETLoungeSerializer(filter_for_group, many=True)
        return Response(serializer.data)