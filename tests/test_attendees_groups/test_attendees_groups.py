import pathlib
import os
from rest_framework import status
from ..test_setup import TestSetUp

class TestAttendeesGroups(TestSetUp):
    
    add_attendees_url = '/api/v1.0/attendees_group/'
    get_groups_attendees_url = '/api/v1.0/attendees_group/'
    delete_groups_attendees_url = '/api/v1.0/attendees_group/1/delete_group_attendees/'

    def test_add_attendees(self):
        BASE_PATH = pathlib.Path(__file__).resolve().parent.parent.parent
        URL_PATH_FILE = os.path.join(BASE_PATH, 'tests.csv')

        self.assertEqual(os.path.exists(URL_PATH_FILE), True)

        response = self.client.post(
            self.add_attendees_url,
            {
                'name': 'Attendees FEMEG',
                'file': open(URL_PATH_FILE, 'rb'),
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def test_get_groups_attendees(self):

        self.test_add_attendees()

        response = self.client.get(
            self.get_groups_attendees_url
        )

        self.assertEqual(
            response.data,
            [{
                'id': 1,
                'name': 'Attendees FEMEG',
                'total': 2
            }]
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response