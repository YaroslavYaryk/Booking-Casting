from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import EventSerializer
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    # RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from event.services import handle_event
from contract.models import Contract


@api_view(["GET"])
def index(request):
    return Response({"message": "HELLO WORLD"})


class EventUserList(ListAPIView):
    serializer_class = EventSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Contract.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
