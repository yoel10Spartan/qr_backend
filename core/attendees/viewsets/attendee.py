import time
import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import Attendee
from .lounge import LoungeManagement
from ..serializers import (
    AttendeeSerializer,
    GETAttendeeLoungeSerializer
)
from ...messages.spanish import *

from core.events.models import Event
from core.events.viewsets import EventManagement

class AttendeBase:
    model = Attendee
    
    def __init__(self, id) -> None:
        self.id = id

class AttendeeManagement(AttendeBase):
    data = []
    
    def __init__(self, id) -> None:
        super().__init__(id)
    
    def get_queryset(self) -> Attendee:
        return self.model.objects.get(id=self.id)
    
    def get_queryfilter(self):
        return self.model.objects.filter(id=self.id)
    
    @classmethod
    def get_attendees_for_group(cls, id):
        return cls.model.objects \
                .filter(attendeesgroup__id = id)
    
    @classmethod
    def get_attendees_whith_launge(cls, id_group):
        return cls.get_attendees_for_group(id_group) \
                .filter(lounge__isnull=False)
    
    @classmethod
    def create(cls, **kwargs):
        values = {
            'id_qr': kwargs['ID'],
            'name': kwargs['NOMBRE'],
            'last_name': kwargs['APELLIDOS'],
            'email': 'correo@email.com',
        }
        
        if cls.model.objects.filter(**values).exists():
            return

        cls.data.append(values)
        return cls.model.objects.create(**values)
    
    def add_to_lounge(self, id):
        lounge = LoungeManagement(id)
        lounge.add_lounge(self.get_queryset())
        return True

    @classmethod
    def delete(cls, **reference):
        cls.model.objects.filter(**reference).delete()

class AttendeeQRManagement(AttendeBase):

    def __init__(self, id) -> None:
        super().__init__(id)

    def get_queryset(self) -> Attendee:
        return self.model.objects.get(id_qr=self.id)
    
    def get_queryfilter(self):
        return self.model.objects.filter(id_qr=self.id)

    @property
    def is_entry(self):
        attendee = self.get_queryset()
        return attendee.entrie
    
    @property
    def is_out(self):
        attendee = self.get_queryset()
        return attendee.output
    
    def set_datetime_entrie(self):
        attendee = self.get_queryset()
        
        attendee.entrie_datetime = datetime.datetime.now()
        attendee.save()
        
    def set_datetime_output(self):
        attendee = self.get_queryset()
        
        attendee.output_datetime = datetime.datetime.now()
        attendee.save()
        
    def get_elapsed_time(self, datetime_entrie, datetime_out):
        datetime_elapsed = (datetime_out - datetime_entrie)
        convert_time = str(datetime_elapsed).split('.')[0]
        time_elapsed = time.strptime(convert_time, "%H:%M:%S")
        hours = time_elapsed.tm_hour
        minutes = time_elapsed.tm_min
        seconds = time_elapsed.tm_sec
        return [ hours, minutes, seconds ]
    
    def update_hours(self):
        attendee = self.get_queryset()
        
        datetime_entrie = attendee.entrie_datetime
        datetime_out = attendee.output_datetime
        
        hours = round(((datetime_out - datetime_entrie).total_seconds() / 3600), 2)
        
        attendee.hours = hours
        attendee.save()
    
    def dial_entry(self, id_event, id_operator):
        attendee = self.get_queryset()
        
        validate_event = EventManagement(id_event) \
            .validate_event(self.id, id_operator)
        
        if not validate_event:
            return [ False, DETAIL_USER_OPERATOR_EVENT_ERROR, status.HTTP_400_BAD_REQUEST ]
        
        if not self.is_out:
            return [ False, DETAIL_FAIL_ENTRY, status.HTTP_400_BAD_REQUEST ]
          
        self.add_or_update_lounge(id_operator)
        
        attendee.entrie = True
        attendee.output = False
        
        self.increase_aforo()
        self.increase_total_aforo()
        
        attendee.save()
        self.set_datetime_entrie()
        return [ True, DETAIL_SUCCESS_ENTRY, status.HTTP_200_OK ]
        
    def dial_out(self, id_event, id_operator):
        attendee = self.get_queryset()
        
        validate_event = EventManagement(id_event) \
            .validate_event(self.id, id_operator)
        
        if not attendee:
            return [ False, DETAIL_USER_NOT_ADDED_LOUNGE, status.HTTP_400_BAD_REQUEST ]
        
        if not self.is_entry:
            return [ False, DETAIL_FAIL_OUT, status.HTTP_400_BAD_REQUEST ]
        
        attendee.output = True
        attendee.entrie = False
        attendee.save()
        self.set_datetime_output()
        self.update_hours()
        self.decrease_aforo()
        
        return [ True, DETAIL_SUCCESS_OUT, status.HTTP_200_OK ]
    
    def increase_total_aforo(self):
        attendee = self.get_queryset()
        if attendee.hours != '00:00:00':
            return
        lounge_now = LoungeManagement.search(attendees=self.get_queryset())
        lounge = LoungeManagement(lounge_now.first().id)
        lounge.increase_total_aforo()
    
    def increase_aforo(self):
        lounge_now = LoungeManagement.search(attendees=self.get_queryset())
        lounge = LoungeManagement(lounge_now.first().id)
        lounge.increase_aforo()
    
    def decrease_aforo(self):
        lounge_now = LoungeManagement.search(attendees=self.get_queryset())
        lounge = LoungeManagement(lounge_now.first().id)
        lounge.decrease_aforo()
    
    def add_or_update_lounge(self, id_operator):
        lounge_now = LoungeManagement.search(attendees=self.get_queryset())
        lounge_now_operator = LoungeManagement.search(operators__id=id_operator)
        
        if lounge_now.exists():
            if lounge_now.first().id == lounge_now_operator.first().id:
                return
            lounge_before = LoungeManagement(lounge_now.first().id)
            self.decrease_aforo()
            lounge_before.remove_attendee(self.get_queryset())
            
        lounge = LoungeManagement(lounge_now_operator.first().id)
        lounge.add_lounge(self.get_queryset())
        
    def add_attende_group_anonymous(self, id_operator):
        event = Event.objects.filter(operators__id = id_operator)
        if not event.exists(): return
        attendees_group = event.first().attendees_group
        attendees = attendees_group.attendees
        attendees.add(self.get_queryset())

class AttendeeViewSet(viewsets.ModelViewSet):
    serializer_class = AttendeeSerializer
    queryset = Attendee.objects.all()
    
    @action(methods=['POST'], detail=False)
    def add_lounge(self, request, *args, **kwargs):
        id_attendee = request.data['id_attendee']
        id_lounge = request.data['id_lounge']
        
        attendee_management = AttendeeManagement(id_attendee)
        attendee_management.add_to_lounge(id_lounge)
        
        return Response({'ok': True}, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['PUT'], detail=True)
    def entry_mark(self, request, pk):
        id_event = request.data['id_event']
        id_operator = request.data['id_operator']
        
        try:
            attendee_management = AttendeeQRManagement(pk)
            ok, detail, status_http = attendee_management.dial_entry(id_event, id_operator)
        except Attendee.DoesNotExist:
            values = {
                'id': pk,
                'nombre': 'anonymous',
                'apellidos': 'anonymous',
                'correo electronico': 'anonymous',
            }
            
            attendee = AttendeeManagement.create(**values)
            
            attendee_management = AttendeeQRManagement(pk)
            attendee_management.add_attende_group_anonymous(id_operator)
            ok, detail, status_http = attendee_management.dial_entry(id_event, id_operator)
        
        return Response({
            'ok': ok, 
            'detail': detail
        }, 
            status=status_http
        )
    
    @action(methods=['PUT'], detail=True)
    def exit_mark(self, request, pk):
        id_event = request.data['id_event']
        id_operator = request.data['id_operator']
        
        attendee_management = AttendeeQRManagement(pk)
        ok, detail, status_http = attendee_management.dial_out(id_event, id_operator)

        return Response({
            'ok': ok,
            'detail': detail
        },
            status=status_http
        )
        
    @action(methods=['GET'], detail=True)
    def get_attendees_for_group(self, request, pk):
        
        attendees = AttendeeManagement.get_attendees_for_group(pk)
        serializer = GETAttendeeLoungeSerializer(attendees, many=True)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
        
    @action(methods=['POST'], detail=False)
    def add_anonymous_attendee(self, request):
        id_qr = request.data['id_qr']
        
        values = {
            'id': id_qr,
            'nombre': 'anonymous',
            'apellidos': 'anonymous',
            'correo electronico': 'anonymous',
        }
        
        attendee = AttendeeManagement.create(**values)
        return Response({
            'ok': True,
            'id_attendee': attendee.id
        })