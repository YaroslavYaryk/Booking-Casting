from rest_framework.serializers import ModelSerializer
from contract.models import (
    Contract,
    ContractEventTeam,
    ContractEventRentalProducts,
    ContractRentalProducts,
    ContractTimeClock,
    ArtistTeamEvent,
)
from event.models import Event
from django.utils.html import strip_tags
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer,
)
from venue.models import VenuePictures


class EventSerializer(ModelSerializer):

    company = SerializerMethodField()
    customer = SerializerMethodField()
    artist = SerializerMethodField()
    venue = SerializerMethodField()
    venue_image = SerializerMethodField()

    class Meta:
        model = Contract
        # fields = "__all__"
        exclude = ("contract",)

    def get_company(self, instance):
        return instance.company.name

    def get_customer(self, instance):
        return instance.customer.name

    def get_artist(self, instance):
        return instance.artist.name

    def get_venue(self, instance):
        return instance.venue.name

    def get_venue_image(self, instance):
        venue = instance.venue
        venue_pictures = VenuePictures.objects.filter(venue=venue)
        if venue_pictures:
            return venue_pictures.first().file.url
        return None


class EventTeamSerializer(ModelSerializer):

    user = SerializerMethodField()
    user_email = SerializerMethodField()

    def get_user(self, instance):
        return instance.user.get_full_name()

    def get_user_email(self, instance):
        return instance.user.email

    class Meta:
        model = ContractEventTeam
        fields = "__all__"


class ContractProductSerializer(ModelSerializer):
    class Meta:
        model = ContractRentalProducts
        fields = "__all__"


class ContractEventRentalProductsSerializer(ModelSerializer):

    rental_products = ContractProductSerializer()

    class Meta:
        model = ContractEventRentalProducts
        fields = "__all__"


class ContractTimeClockSerializer(ModelSerializer):

    event_time_clock = SerializerMethodField("get_event_time_clock")

    def get_event_time_clock(self, instance):

        return [
            {
                "id": el.id,
                "start_time": el.start_time,
                "end_time": el.end_time,
                "action": el.action,
            }
            for el in instance.event_time_clock()
        ]

    class Meta:
        model = ContractTimeClock
        fields = ("event_time_clock",)
        # exclude = ("day_schedule",)


class ArtistTeamEventSerializer(ModelSerializer):

    team_users = SerializerMethodField("get_team_users")

    def get_team_users(self, instance):

        return [
            {
                "id": el.id,
                "name": el.get_full_name(),
                "email": el.email,
            }
            for el in instance.artist_event_team()
        ]

    class Meta:
        model = ArtistTeamEvent
        fields = ("team_users",)
