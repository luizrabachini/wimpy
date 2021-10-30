from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):

    def get(self, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
