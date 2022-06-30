from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from core.users.models import User

class TestSetUp(APITestCase):
    
    faker = Faker()
    name = faker.name()
    username = 'randomusername'
    password = faker.password()
    object_user = {
        'id': 1, 
        'name': name, 
        'username': username,
        'is_staff': True, 
        'is_operator': False,
    }

    login_url = '/api/v1.0/auth/login/'
    
    def setUp(self):    

        # CREATE
        User.objects.create_superuser(
            username=self.username,
            name=self.name,
            password=self.password,
        )        

        # LOGIN
        response_login = self.client.post(
            self.login_url,
            {
                'username': self.username,
                'password': self.password
            },
            format='json'
        )

        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

        self.access = response_login.data['access']
        self.refresh = response_login.data['refresh']
        self.user = response_login.data['user']
        
        self.assertEqual(type(self.access), str)
        self.assertEqual(type(self.refresh), str)
        self.assertEqual(self.user, self.object_user)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        return super().setUp()

    # def test_example(self):
    #     return True