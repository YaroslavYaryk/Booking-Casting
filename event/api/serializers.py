from rest_framework.serializers import ModelSerializer
from contract.models import Contract
from event.models import Event
from django.utils.html import strip_tags
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer,
)


class EventSerializer(ModelSerializer):

    company = SerializerMethodField()
    customer = SerializerMethodField()
    artist = SerializerMethodField()
    venue = SerializerMethodField()

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
