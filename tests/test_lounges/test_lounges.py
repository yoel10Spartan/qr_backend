from rest_framework import status
from ..test_attendees_groups.test_attendees_groups import TestAttendeesGroups
import unittest

class TestLounges(TestAttendeesGroups):
    create_lounge_url = '/api/v1.0/lounge/'
    get_lounges_for_group_url = '/api/v1.0/lounge/1/get_for_group/'
    get_list_attendees_with_lounge_url = '/api/v1.0/attendees_group/1/get_attends_with_lounge/'

    def test_create_lounge(self):
        self.test_add_attendees()

        response = self.client.post(
            self.create_lounge_url,
            {
                "name": "Salon 5",
                "aforo": 30,
                "attendees_group": 1
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_get_lounges_for_group(self):
        self.test_create_lounge()

        response = self.client.get(
            self.get_lounges_for_group_url,
        )

        self.assertEqual(
            response.data,
            [
                {
                    'id': 1,
                    'name': 'Salon 5',
                    'aforo_current': 0,
                    'aforo': 30
                }
            ]
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)