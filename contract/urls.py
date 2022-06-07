from django.urls import path
from .views import (
    create_contract,
    preview_artist_contract,
    get_contract,
    save_artist_contract_data,
    get_visible_contracted_artists,
    cancel_contract,
    edit_contract,
    get_contract_view,
    # preview_artist_contract_view,
    hide_contract,
    get_hidden_contracts_list,
    unhide_contract,
    get_visible_contracts_for_user,
    get_hidden_contracts_for_user,
    customer_create_contract_from_user,
    user_edit_contract,
    hide_contract_from_user,
    unhide_contract_from_user,
    create_contract_with_errors,
    create_contract_with_errors_from_user,
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
    # path(
    #     "<contract_id>/preview_contract/",
    #     preview_artist_contract_view,  # when click discard we redirect to back to customer details
    #     name="preview_artist_contract_view",
    # ),
    path("get_contract/", get_contract, name="customer_get_contract_one"),
    path("get_contract/<contract_id>/", get_contract, name="customer_get_contract"),
    path(
        "get_contract_view/<contract_id>/",
        get_contract_view,
        name="customer_get_contract_view",
    ),
    path("save_contract_data/", save_artist_contract_data, name="save_contract_data"),
    path(
        "save_contract_data/<event_artist_id>/<date>/<honorar>/<payment_methods>/<comment>/page_height/<page_heights>/",
        save_artist_contract_data,
        name="save_contract_data",
    ),
    path(
        "<customer_id>/get_contracted_artists/<date>/",
        get_visible_contracted_artists,
        name="get_all_contracted_artists",
    ),
    path(
        "<customer_id>/get_hidden_artists/",
        get_hidden_contracts_list,
        name="get_hidden_contracts_list",
    ),
    path(
        "<contract_id>/cancel_contract/<redirect_link>/",
        cancel_contract,
        name="cancel_contract",
    ),
    path("<contract_id>/hide_contract/<date>/", hide_contract, name="hide_contract"),
    path("<contract_id>/unhide_contract/", unhide_contract, name="unhide_contract"),
    path("<contract_id>/edit_contract/", edit_contract, name="customer_edit_contract"),
    # user_contracts
    path(
        "user_contracts/<user_id>/visible/",
        get_visible_contracts_for_user,
        name="get_visible_contracts_for_user",
    ),
    path(
        "user_contracts/<user_id>/hidden/",
        get_hidden_contracts_for_user,
        name="get_hidden_contracts_for_user",
    ),
    path(
        "<user_id>/create_contract_from_user/",
        customer_create_contract_from_user,
        name="customer_create_contract_from_user",
    ),
    path(
        "<contract_id>/user_edit_contract/",
        user_edit_contract,
        name="user_edit_contract",
    ),
    path(
        "<contract_id>/hide_contract_from_user/",
        hide_contract_from_user,
        name="hide_contract_from_user",
    ),
    path(
        "<contract_id>/unhide_contract_from_user/",
        unhide_contract_from_user,
        name="unhide_contract_from_user",
    ),
    path(
        "<contract_id>/confirmation_contract_with_errors/",
        create_contract_with_errors,
        name="create_contract_with_errors",
    ),
    path(
        "<contract_id>/user_confirmation_with_errors/",
        create_contract_with_errors_from_user,
        name="create_contract_with_errors_from_user",
    ),
]
