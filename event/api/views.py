from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ContractEventRentalProductsSerializer,
    EventSerializer,
    EventTeamSerializer,
    ContractTimeClockSerializer,
    ArtistTeamEventSerializer,
)
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
from contract.models import (
    Contract,
    ContractEventTeam,
    ContractEventRentalProducts,
    ContractTimeClock,
    ArtistTeamEvent,
)
from .services import handle_event as api_event_handle


@api_view(["GET"])
def index(request):
    return Response({"message": "HELLO WORLD"})


class EventUserList(ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = api_event_handle.get_event_for_user(request.user)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)


class EventUserDetails(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk):
        queryset = Contract.objects.get(pk=pk)
        serializer = EventSerializer(queryset)
        return Response(serializer.data)


class ContractEventTeamAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, contract_id):
        queryset = ContractEventTeam.objects.filter(contract__id=contract_id)
        serializer = EventTeamSerializer(queryset, many=True)
        return Response(serializer.data)


class ContractEventRentalProductsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, contract_id):
        queryset = ContractEventRentalProducts.objects.filter(contract__id=contract_id)
        serializer = ContractEventRentalProductsSerializer(queryset, many=True)
        return Response(serializer.data)


class ContractTimeClockAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, contract_id):
        queryset = ContractTimeClock.objects.filter(contract__id=contract_id)
        serializer = ContractTimeClockSerializer(queryset, many=True)
        return Response(
            serializer.data[0].get("event_time_clock")
            if len(serializer.data)
            else serializer.data
        )


class ArtistTeamEventAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, contract_id):
        queryset = ArtistTeamEvent.objects.filter(contract__id=contract_id)
        serializer = ArtistTeamEventSerializer(queryset, many=True)
        return Response(
            serializer.data[0].get("team_users")
            if len(serializer.data)
            else serializer.data
        )
