from django.urls import path


from .views import (
    MyVenueListView,
    add_new_venue,
    add_user_permission_to_change_or_see_venue,
    change_details_venue,
    change_user_permission_to_change_or_see_venue,
    delete_user_from_venue_changeble,
    delete_venue,
    delete_venue_picture,
    get_venue_contracts,
    get_venue_details,
    send_request_to_change_venue,
    upload_picture_handle,
    invite_user,
    get_venue_hidden_contracts,
    hide_artist_contract,
    unhide_artist_contract,
)

urlpatterns = [
    path("", MyVenueListView.as_view(), name="get_my_venues"),
    path("add_venue/", add_new_venue, name="add_new_venue"),
    path("<venue_id>/details/", get_venue_details, name="get_venue_details"),
    path("<venue_id>/update_venue/", change_details_venue, name="change_details_venue"),
    path("<venue_id>/delete_venue/", delete_venue, name="delete_venue"),
    # send request to change
    path(
        "<venue_id>/send_request_to_change/",
        send_request_to_change_venue,
        name="send_request_to_change_venue",
    ),
    # add permission to see or change
    path(
        "add_permission_venue/",
        add_user_permission_to_change_or_see_venue,
        name="add_user_permission_to_change_or_see_venue",
    ),
    path(
        "add_permission_venue/<venue_id>/<user_phone>/<perm_type>/",
        add_user_permission_to_change_or_see_venue,
    ),
    # change permission to see or change
    path(
        "change_permission_venue/",
        change_user_permission_to_change_or_see_venue,
        name="change_user_permission_to_change_or_see_venue",
    ),
    path(
        "change_permission_venue/<access_id>/<perm_type>/",
        change_user_permission_to_change_or_see_venue,
    ),
    # delete from changeble
    path(
        "<venue_id>/delete_user_permissions/<user_id>/",
        delete_user_from_venue_changeble,
        name="delete_user_from_venue_changeble",
    ),
    # picture handle
    path(
        "<venue_id>/upload_picture/",
        upload_picture_handle,
        name="upload_picture_handle",
    ),
    path(
        "<venue_id>/delete_picture/<picture_id>/",
        delete_venue_picture,
        name="delete_venue_picture",
    ),
    # venue events
    path(
        "<venue_id>/all_contracts/<date>/",
        get_venue_contracts,
        name="get_venue_contracts",
    ),
    path(
        "<venue_id>/hidden_venue_contracts/",
        get_venue_hidden_contracts,
        name="get_hidden_contracts_venue",
    ),
    # invite user
    path("invite_user/", invite_user, name="venue_invite_user"),
    path("invite_user/<venue_id>/<user_email>/", invite_user, name="venue_invite_user"),
    # hide / unhide contract
    path(
        "<contract_id>/hide_contract_venue/<date>/",
        hide_artist_contract,
        name="hide_contract_venue",
    ),
    path(
        "<contract_id>/unhide_contract_venue/",
        unhide_artist_contract,
        name="unhide_contract_venue",
    ),
]
