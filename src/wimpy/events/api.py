from typing import Dict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from wimpy.events.serializers import EventSerializer

__all__ = ['EventAPIView']


class EventAPIView(APIView):

    permission_classes = [IsAuthenticated]

    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        data: Dict = {
            'application_id': request.user.username
        }
        data.update(request.data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        # To DO: register event here
        return Response(status=status.HTTP_201_CREATED)
