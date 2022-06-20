from django.urls import path

from .views import (
    index,
    EventUserList,
    EventUserDetails,
    ContractEventTeamAPI,
    ContractEventRentalProductsAPI,
    ContractTimeClockAPI,
    ArtistTeamEventAPI,
)

urlpatterns = [
    path("", index),
    path("list/", EventUserList.as_view()),
    path("list/<pk>/", EventUserDetails.as_view()),
    path("list/<contract_id>/event_team/", ContractEventTeamAPI.as_view()),
    path(
        "list/<contract_id>/rental_products/", ContractEventRentalProductsAPI.as_view()
    ),
    path("list/<contract_id>/time_clock/", ContractTimeClockAPI.as_view()),
    path("list/<contract_id>/artist_team/", ArtistTeamEventAPI.as_view()),
]
