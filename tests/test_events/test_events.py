from rest_framework import status
from ..test_attendees_groups.test_attendees_groups import TestAttendeesGroups

class TestEvents(TestAttendeesGroups):
    create_event_url = '/api/v1.0/events/'
    get_all_events_url = '/api/v1.0/events/'
    get_aforo_url = '/api/v1.0/events/1/get_total_aforo/'
    get_statistics_url = '/api/v1.0/events/1/get_statistics/'

    def test_create_event(self):
        self.test_add_attendees()

        response = self.client.post(
            self.create_event_url,
            {
                "name": "Congreso FEMEG",
                "place": "Santa Ana",
                "start_date": "2022-07-20",
                "finish_date": "2022-07-23",
                "total_hours": 150,
                "count_trade_show_hours": False,
                "aforo": 256,
                "attendees_group": 1
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_events(self):
        self.test_create_event()

        response = self.client.get(
            self.get_all_events_url
        )

        self.assertEqual(
            response.data,
            [
                {
                    'id': 1, 
                    'name': 'Congreso FEMEG', 
                    'group_users': 'Attendees FEMEG', 
                    'group_users_id': 1, 
                    'place': 'Santa Ana', 
                    'date': '2022-07-23', 
                    'not_hours': True, 
                    'count_trade_show_hours': False
                }
            ]
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_aforo(self):
        self.test_create_event()
       
        response = self.client.get(
            self.get_aforo_url
        )

        self.assertEqual(
            response.data,
            {'aforo_current': 0, 'aforo_total': 256}    
        )

    def test_get_statistics_url(self):
        self.test_create_event()
        
        response = self.client.get(
            self.get_statistics_url
        )

        self.assertEqual(
            response.data,
            {
                'aforo': 256, 
                'asistentes': 2, 
                'entradas_totales': 0, 
                'salidas_totales': 0, 
                'codigos_no_usados': 2
            }
        )