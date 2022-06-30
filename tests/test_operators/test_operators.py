from rest_framework import status
from ..test_lounges.test_lounges import TestLounges
from ..test_events.test_events import TestEvents
from core.operators.models import Operator

class TestOperators(TestLounges, TestEvents):

    create_operator_url = '/api/v1.0/operators/'
    delete_operator_url = '/api/v1.0/operators/1/'
    update_lounge_operator_url = '/api/v1.0/operators/1/update_lounge/'
    get_event_url = '/api/v1.0/operators/2/get_event/'

    def test_create_operator(self):
        self.test_create_lounge()
        self.test_create_event()

        response = self.client.post(
            self.create_operator_url,
            {
                "name": "Yoel",
                "id_lounge": 1,
                "id_event": 1
            },
            format='json'
        )

        self.assertEqual(response.data, {'ok': True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_delete_operator(self):
        self.test_create_operator()

        response = self.client.delete(self.delete_operator_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_lounge_operator(self):
        self.test_create_operator()
        self.test_create_lounge()

        response = self.client.put(
            self.update_lounge_operator_url,
            {
                "id_lounge": 2
            }
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        operator = Operator.objects.filter(lounge__id=2)
        self.assertEqual(operator.exists(), True)

    def test_get_event(self):
        self.test_create_operator()
        
        response = self.client.get(
            self.get_event_url
        )

        self.assertEqual(
            response.data,
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
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )