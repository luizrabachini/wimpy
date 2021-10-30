from django.urls import reverse
from rest_framework import status


class TestHealthCheckAPIView:

    def test_healthcheck_status_code(self, client):
        response = client.get(reverse('healthcheck:all'))
        assert response.status_code == status.HTTP_200_OK
