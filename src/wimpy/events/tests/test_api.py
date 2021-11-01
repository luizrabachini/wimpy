import pytest
from django.urls import reverse
from rest_framework import status

from wimpy.events.models import Event


@pytest.mark.django_db
class TestEventAPIView:

    def test_should_register_new_event(self, valid_event_data, auth_client):
        assert Event.objects.count() == 0
        response = auth_client.post(
            reverse('events:events'),
            valid_event_data,
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 1

    def test_should_authorize_client(self, valid_event_data, client):
        response = client.post(
            reverse('events:events'),
            valid_event_data,
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_validate_data(self, valid_event_data, auth_client):
        valid_event_data['data'] = {
            'host': 'localhost',
        }
        response = auth_client.post(
            reverse('events:events'),
            valid_event_data,
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
