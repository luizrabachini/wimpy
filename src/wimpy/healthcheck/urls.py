from django.urls import path

from wimpy.healthcheck.api import HealthCheckAPIView

urlpatterns = [
    path(
        '',
        HealthCheckAPIView.as_view(),
        name='healthcheck'
    ),
]
