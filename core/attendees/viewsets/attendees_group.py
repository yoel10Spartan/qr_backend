import pathlib
import csv
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import AttendeesGroup
from ..serializers import (
    AttendeeGroupSerializer, 
    GETAttendeeGroupSerializer,
    AttendeeWithLoungeSerializer
)
from .attendee import AttendeeManagement, Attendee
from ...messages.spanish import *

class AttendeeGroupManagement:
    model = AttendeesGroup
    
    def __init__(self, id) -> None:
        self.id = id
    
    def get_queryset(self):
        return AttendeesGroup.objects.get(pk=self.id)
    
    def get_path_file(self):
        return self.get_queryset().file.path
    
    def is_format_csv(self):
        suffix = pathlib.Path(self.get_path_file()).suffix
        return suffix == '.csv'
    
    def read_csv(self):
        dict_reader = []
        if self.is_format_csv():
            file = open(self.get_path_file(), 'r')
            dict_reader = csv.DictReader(file)
        return dict_reader
    
    def add_attendee(self, attendee: Attendee):
        attendees_group = self.get_queryset()
        attendees_group.attendees.add(attendee)
        attendees_group.save()
    
    def create_attendee(self):
        for attendee in self.read_csv():
            attendee = AttendeeManagement.create(**attendee)
            self.add_attendee(attendee)
    
    def get_attends_with_lounge(self):
        return AttendeeManagement.get_attendees_whith_launge(self.id)
        
    def start(self):
        self.create_attendee()
        
    def add_lounge(self, lounge):
        attendee_group = self.get_queryset()
        attendee_group.lounges.add(lounge)
        attendee_group.save()
            
    @staticmethod
    def create(**kwargs):
        return AttendeesGroup.objects.create(**kwargs)

    def delete_group_attendees(self):
        AttendeeManagement.delete(attendeesgroup__id=self.id)
        self.get_queryset().delete()
    
class AttendeeGroupViewSet(viewsets.ModelViewSet):
    serializer_class = AttendeeGroupSerializer
    queryset = AttendeesGroup.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        attendee_group_management = AttendeeGroupManagement(serializer.data['id'])
        if not attendee_group_management.is_format_csv():
            return Response(
                {
                    'ok': False,
                    'detail': DETAIL_FORMAT_NOT_VALID,
                }, 
                status=status.HTTP_400_BAD_REQUEST, 
            )
        
        attendee_group_management.start()
        
        return Response({'ok': True}, status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = GETAttendeeGroupSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=['GET'], detail=True)
    def get_attends_with_lounge(self, request, pk):
        attendee_group_management = AttendeeGroupManagement(pk).get_attends_with_lounge()
        attendee_with_lounge_serializer = AttendeeWithLoungeSerializer(attendee_group_management, many=True)
        return Response(attendee_with_lounge_serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False)
    def add_anonymous_attendee_group(self, request):
        id_attendee = request.data['id_attendee']
        id_attendee_group = request.data['id_attendee_group']
        
        attendee_manegement = AttendeeManagement(id_attendee)
        AttendeeGroupManagement(id_attendee_group) \
            .add_attendee(attendee_manegement.get_queryset())
            
        return Response({'ok': True}, status=status.HTTP_200_OK)

    @action(methods=['DELETE'], detail=True)
    def delete_group_attendees(self, request, pk):
        AttendeeGroupManagement(pk).delete_group_attendees()
        return Response(status=status.HTTP_204_NO_CONTENT)