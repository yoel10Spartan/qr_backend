from rest_framework import status
from core.messages.spanish import *
from ..test_operators.test_operators import TestOperators

class TestAttendees(TestOperators):
    add_attendee_lounge_url = '/api/v1.0/attendees/add_lounge/'
    mark_entry_url = '/api/v1.0/attendees/1/entry_mark/'
    mark_out_url = '/api/v1.0/attendees/1/exit_mark/'
    get_attendee_list_url = '/api/v1.0/attendees/1/get_attendees_for_group/'
    get_attendees_with_hours_url = '/api/v1.0/events/1/get_attendees/'

    def test_add_attendee_lounge(self):
        self.test_add_attendees()
        self.test_create_lounge()

        response = self.client.post(
            self.add_attendee_lounge_url,
            {
                "id_attendee": 1,
                "id_lounge": 1
            }
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_list_attendees_with_lounge(self):

        self.test_add_attendee_lounge()

        response = self.client.get(
            self.get_list_attendees_with_lounge_url,
        )

        self.assertEqual(
            response.data,
            [
                {
                    'id': 1,
                    'id_qr': 1, 
                    'name': 'Yoel',
                    'lounge': 'Salon 5'
                }
            ]
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def mark_entry(self):
        self.test_create_operator()
        
        return self.client.put(
            self.mark_entry_url,
            { 
                "id_event": 1,
                "id_operator": 1
            },
            format='json',
        )

    def test_mark_entry_attendee(self):
        
        response = self.mark_entry()

        self.assertEqual(
            response.data['detail'], DETAIL_SUCCESS_ENTRY
        )

        response = self.mark_entry()

        self.assertEqual(
            response.data['detail'], DETAIL_FAIL_ENTRY
        )

    def mark_out(self):
        self.test_create_operator()
        
        return self.client.put(
            self.mark_out_url,
            { 
                "id_event": 1,
                "id_operator": 1
            },
            format='json',
        )

    def test_mark_out_attendee(self):
        self.mark_entry()

        response = self.mark_out()

        self.assertEqual(
            response.data['detail'], DETAIL_SUCCESS_OUT
        )

        response = self.mark_out()

        self.assertEqual(
            response.data['detail'], DETAIL_FAIL_OUT
        )

    def test_get_attendee_list(self):
        self.test_add_attendees()

        response = self.client.get(self.get_attendee_list_url)

        self.assertEqual(
            response.data,
            [
                {
                    'id': 1,
                    'id_qr': 1,
                    'name': 'Yoel Munoz Zecua'
                },
                {
                    'id': 2,
                    'id_qr': 2,
                    'name': 'Santiago Munoz Zecua'
                }
            ]
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_attendees_with_hours(self):
        self.test_create_event()

        response = self.client.get(
            self.get_attendees_with_hours_url
        )

        self.assertEqual(
            response.data,
            [
                {
                    'id': 1, 
                    'name': 'Yoel Munoz Zecua', 
                    'id_qr': 1, 
                    'total_hours': 150, 
                    'hours_covered': 0.0, 
                    'hours_left': 150.0
                }, 
                {
                    'id': 2, 
                    'name': 'Santiago Munoz Zecua', 
                    'id_qr': 2, 'total_hours': 150, 
                    'hours_covered': 0.0, 
                    'hours_left': 150.0
                }
            ]
        )