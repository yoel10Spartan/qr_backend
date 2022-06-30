import os
import xlsxwriter
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse
from core.operators.serializers.operators import OperatorsSerializer

from ..models import Event
from ..serializers import EventSerializer

class EventManagement:
    event = None
    model = Event
    
    def __init__(self, id) -> None:
        self.id = id
        
    def get_queryset(self):
        return self.model.objects.get(id=self.id)

    def get_total_aforo(self):
        return self.get_queryset().aforo
    
    def add_operator(self, operator):
        event = self.get_queryset()
        event.operators.add(operator)
        event.save()
        
    def validate_event(self, id_attendee, id_operator):
        return self.model.objects \
            .filter(pk=self.id) \
            .filter(
                Q(attendees_group__attendees__id_qr=id_attendee),
                Q(operators__id=id_operator)
            ).exists()
            
    def get_aforo_total(self):
        aforo_current = 0
        aforo_total = 0
        
        lounges = self.get_queryset().attendees_group.lounges.all()
        for i in lounges:
            aforo_current += i.aforo_current
            # aforo_total += i.aforo
            
        return {
            'aforo_current': aforo_current,
            'aforo_total': self.get_queryset().aforo
        }
    
    def get_all_attendees(self):
        _attendees = []

        event = self.get_queryset()

        total_hours = event.total_hours
    
        attendees = event.attendees_group.attendees.all()
        
        for i in attendees:
            hours_current = round((float(i.hours)*100)/total_hours, 1)
            data = {
                'id': i.id,
                'name': ' '.join([i.name, i.last_name]),
                'id_qr': i.id_qr,
                'total_hours': total_hours,
                'hours_covered': hours_current,
                'hours_left': 100 - hours_current
            }
            _attendees.append(data)
            
        return _attendees
    
    def get_statistics(self):
        event = self.get_queryset()
        
        attendees = event.attendees_group.attendees
        
        aforo = event.aforo
        attendees_total = attendees.count()
        total_tickets = 0
        total_exits = attendees.filter(output_datetime__isnull=False).count()
        
        for i in event.attendees_group.lounges.all():
            total_tickets += i.aforo_current
        
        unused_codes = attendees \
                        .filter(
                            output_datetime__isnull=True, 
                            entrie_datetime__isnull=True
                        ) \
                        .count()
    
        return {
            'aforo': aforo,
            'asistentes': attendees_total,
            'entradas_totales': total_tickets,
            'salidas_totales': total_exits,
            'codigos_no_usados': unused_codes
        }
        
    @classmethod
    def search(cls, **kwargs):
        return cls.model.objects.filter(**kwargs)
    
    @classmethod
    def get_event_for_operator(cls, operator):
        event = cls.search(operators=operator)
        return EventSerializer(event.first())
    
    def get_operators(self):
        return self.get_queryset().operators.all()

    def delete_event(self):
        ...

    def get_data_excel(self):
        book = xlsxwriter.Workbook(os.getcwd() + '/users.xls')
        sheet = book.add_worksheet()

        header = [
            'id',
            'nombre',
            'apellidos'
            'horas cubiertas',
            'horas faltantes'
        ]

        row = 0
        col = 0
        
        for i in header:
            sheet.write(row, col, i)
            col+=1

        event = self.get_queryset()

        total_hours = event.total_hours
    
        attendees = event.attendees_group.attendees.all()

        row = 1
        col = 0
        
        for i in attendees:
            items = [
                i.id_qr,
                i.name, 
                i.last_name,
                i.hours,
                float(total_hours) - float(i.hours)
            ]

            for j in items:
                sheet.write(row, col, j)
                col+=1
            col=0
            row+=1

        book.close()

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    
    @action(methods=['GET'], detail=True)
    def get_total_aforo(self, request, pk):
        
        event_management = EventManagement(pk)
        
        return Response(
            event_management.get_aforo_total(),
            status=status.HTTP_200_OK
        )
        
    @action(methods=['GET'], detail=True)
    def get_attendees(self, request, pk):
        
        event_management = EventManagement(pk)
        
        return Response(
            event_management.get_all_attendees(),
            status=status.HTTP_200_OK
        )
        
    @action(methods=['GET'], detail=True)
    def get_statistics(self, request, pk):
        
        event_management = EventManagement(pk)
        
        return Response(
            event_management.get_statistics(),
            status=status.HTTP_200_OK
        )
        
    @action(methods=['GET'], detail=True)
    def get_operator_for_event(self, request, pk):
        
        event_management = EventManagement(pk)
        operators = event_management.get_operators()
        
        operators_serializer = OperatorsSerializer(operators, many=True)
        
        return Response(
            operators_serializer.data, 
            status=status.HTTP_200_OK
        )

    @action(methods=['GET'], detail=True)
    def get_data_excel(self, request, pk):

        EventManagement(pk).get_data_excel()

        file_path = os.getcwd() + '/users.xls'

        with open(file_path, 'rb') as f:
           file_data = f.read()
        
        response = HttpResponse(
            file_data, 
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename=usuarios.xls'
        return response

# http://127.0.0.1:8000/api/v1.0/events/16/get_data_excel/