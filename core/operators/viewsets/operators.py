import string
import random
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..db import Operator
from ..serializers import OperatorsSerializer, GETDataOperatorSerializer
from core.attendees.viewsets import LoungeManagement
from core.events.viewsets import EventManagement
from core.users.models import User
from core.events.serializers.events import EventSerializer

class OperatorsManagement:
    model = Operator
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    length_password = 6
    
    def __init__(self, id) -> None:
        self.id = id
    
    def get_queryset(self):
        return self.model.objects.get(pk=self.id)
    
    def get_filterset(self):
        return self.model.objects.filter(pk=self.id)
    
    def create_password(self):
        password = []
        
        random.shuffle(self.characters)
	
        for i in range(self.length_password):
            password.append(random.choice(self.characters))

        random.shuffle(password)
        return ''.join(password)

    def create_username(self, name: str):
        return ''.join([name.lower(), str(random.randint(10, 99))])
    
    def update_lounge(self, id_lounge: int):
        lounge_now = LoungeManagement.search(operators=self.get_queryset())
        
        if lounge_now.exists():
            lounge_before = LoungeManagement(lounge_now.first().id)
            lounge_before.remove_operator(self.get_queryset())
            
        lounge = LoungeManagement(id_lounge)
        lounge.add_operator(self.get_queryset())
    
    @classmethod
    def delete(cls, instance: User):
        name = instance.name
        username = instance.username
        is_operator = True
        
        user = User.objects.filter(
            name=name, 
            username=username, 
            is_operator=is_operator
        )
        
        user.first().delete()
        return True
    
    @classmethod
    def create_account(cls, name: str, id_lounge: int, id_event: int):
        account = {
            'name': name,
            'username': cls.create_username(cls, name),
            'password': cls.create_password(cls), 
            'is_operator': True
        }
        user = User.objects.create_user(**account)
        
        del account['is_operator']
        account['id_user'] = user.id
        operator = cls.model.objects.create(**account)
        
        EventManagement(id_event).add_operator(operator)
        LoungeManagement(id_lounge).add_operator(operator)
        
        return True
    
    @classmethod
    def get_event(cls, pk):
        operator = cls.model.objects.get(id_user=pk)
        return EventManagement.get_event_for_operator(operator)
    
    @classmethod
    def get_data(cls, id_user):
        user = cls.model.objects.filter(id_user=id_user)
        if not user.exists():
            return
        return user.first()
    
class OperatorsViewSet(viewsets.ModelViewSet):
    serializer_class = OperatorsSerializer
    queryset = Operator.objects.filter(is_active=True)
    
    def create(self, request, *args, **kwargs):
        name = request.data['name']
        id_lounge = request.data['id_lounge']
        id_event = request.data['id_event']
        
        OperatorsManagement.create_account(name, id_lounge, id_event)
        return Response({'ok': True}, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        OperatorsManagement.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['PUT'], detail=True)
    def update_lounge(self, request, pk):
        id_lounge = request.data['id_lounge']
        OperatorsManagement(pk).update_lounge(id_lounge)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['GET'], detail=True)
    def get_event(self, request, pk):
        
        event_serializer = OperatorsManagement.get_event(pk)
        
        return Response(event_serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=True)
    def get_data(self, request, pk):
        
        id_user = pk
        operator = OperatorsManagement.get_data(id_user)
        
        operator_serializer = GETDataOperatorSerializer(operator)
        
        return Response(
            operator_serializer.data, 
            status=status.HTTP_200_OK
        )