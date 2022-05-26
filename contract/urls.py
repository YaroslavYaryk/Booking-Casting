from django.urls import path
from .views import (
    create_contract,
    preview_artist_contract,
    get_contract,
    save_artist_contract_data,
    get_all_contracted_artists,
    cancel_contract,
    edit_contract,
)

urlpatterns = [
    path(
        "<customer_id>/create_contract/",
        create_contract,
        name="customer_create_contract",
    ),
    path(
        "<contract_id>/preview_contract/",
        preview_artist_contract,
        name="preview_artist_contract",
    ),
    path("<contract_id>/get_contract/", get_contract, name="customer_get_contract"),
    path("save_contract_data/", save_artist_contract_data, name="save_contract_data"),
    path(
        "save_contract_data/<event_artist_id>/<date>/<honorar>/<payment_methods>/<comment>/",
        save_artist_contract_data,
        name="save_contract_data",
    ),
    path(
        "<customer_id>/get_contracted_artists/",
        get_all_contracted_artists,
        name="get_all_contracted_artists",
    ),
    path("<contract_id>/cancel_contract/", cancel_contract, name="cancel_contract"),
    path("<contract_id>/edit_contract/", edit_contract, name="customer_edit_contract"),
]
