from django.urls import path, include

from .views import (
    MyEventsListView,
    add_event_artist_team,
    add_event_product,
    # add_new_event,
    add_user_to_team,
    # delete_artist_from_event,
    # delete_event,
    delete_event_product,
    delete_user_from_team,
    edit_event_product,
    edit_user_in_team,
    # get_event_artist_list,
    get_event_details,
    get_event_products_list,
    # load_contract_for_event,
    # update_event,
    add_time_clock_to_event,
    remove_time_clock_to_event,
    edit_time_clock_to_event,
    edit_event_artist_team,
    get_my_events,
    confirm_event_product_from_customer,
    load_product_confirmation_page,
)
from .api import urls as event_api

urlpatterns = [
    path("api/", include(event_api)),
    path("list/<date>/", get_my_events, name="get_all_events"),
    # path("add_new/", add_new_event, name="add_new_event"),
    path(
        "<event_id>/details/<time_clock_id>/",
        get_event_details,
        name="get_event_details",
    ),
    # path("<event_id>/update/", update_event, name="update_event"),
    # path("<event_id>/delete/", delete_event, name="delete_event"),
    # path(
    #     "<event_id>/contract/", load_contract_for_event, name="load_contract_for_event"
    # ),
    # path("<event_id>/artists/", get_event_artist_list, name="get_event_artist_list"),
    # path(
    #     "<event_id>/delete_artist/<artist_id>/",
    #     delete_artist_from_event,
    #     name="delete_artist_from_event",
    # ),
    path("<event_id>/add_user_to_team/", add_user_to_team, name="add_user_to_team"),
    path("edit_user_in_team/", edit_user_in_team, name="edit_user_in_team"),
    path(
        "edit_user_in_team/<event_id>/<user_email>/<role>/",
        edit_user_in_team,
        name="edit_user_in_team_full",
    ),
    path(
        "<event_id>/delete_user_from_team/<user_email>/",
        delete_user_from_team,
        name="delete_user_from_team",
    ),
    # event products
    path("<event_id>/add_event_product/", add_event_product, name="add_event_product"),
    path(
        "<event_id>/products_list/",
        get_event_products_list,
        name="get_event_products_list",
    ),
    path(
        "<event_id>/delete_event_product/<product_id>/",
        delete_event_product,
        name="delete_event_product",
    ),
    path(
        "<event_id>/edit_event_product/<product_id>/",
        edit_event_product,
        name="edit_event_product",
    ),
    path(
        "<event_id>/confirmation_page/<product_id>/",
        load_product_confirmation_page,
        name="load_product_confirmation_page",
    ),
    path(
        "<event_id>/customer_confirm_product/<product_id>/",
        confirm_event_product_from_customer,
        name="confirm_event_product_from_customer",
    ),
    # time clock
    path(
        "<event_id>/add_time_clock_to_event/<last_clock_time_id>/",
        add_time_clock_to_event,
        name="add_time_clock_to_event",
    ),
    path(
        "<event_id>/remove_time_clock_to_event/<time_clock_id>",
        remove_time_clock_to_event,
        name="remove_time_clock_to_event",
    ),
    path(
        "<event_id>/edit_time_clock_to_event/<time_clock_id>/",
        edit_time_clock_to_event,
        name="edit_time_clock_to_event",
    ),
    # artist event team users
    path(
        "<event_id>/specify_event_artist_team/",
        add_event_artist_team,
        name="add_event_artist_team",
    ),
    path(
        "edit_event_artist_team/",
        edit_event_artist_team,
        name="edit_event_artist_team",
    ),
    path(
        "edit_event_artist_team/<event_id>/<artist_users_team>/",
        edit_event_artist_team,
        name="edit_event_artist_team_two",
    ),
]
