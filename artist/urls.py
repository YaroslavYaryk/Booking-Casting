from django.urls import path

from .views import (
    MyArtistListView,
    add_new_artist,
    add_user_permission_to_change_or_see,
    change_details_artist,
    change_user_permission_to_change_or_see,
    delete_artist,
    delete_artist_file,
    delete_user_from_changeble,
    get_all_messages,
    get_artist_details,
    handle_change_request,
    send_request_to_change_artist,
    load_tech_rider,
    load_hosp_rider,
    invite_user,
    get_artist_contracts,
    get_hiden_artist_contracts,
    hide_artist_contract,
    unhide_artist_contract,
    index,
)

urlpatterns = [
    # path("all/", ArtistListView.as_view(), name="all_actors"),
    path("my_artists/", MyArtistListView.as_view(), name="all_my_actors"),
    path("add_new_artist/", add_new_artist, name="add_artist"),
    path("<artist_id>/artist_details/", get_artist_details, name="artist_details"),
    path("<artist_id>/update/", change_details_artist, name="change_artist"),
    path(
        "<artist_id>/send_request_to_change/",
        send_request_to_change_artist,
        name="send_request_to_change",
    ),
    path("<artist_id>/delete/", delete_artist, name="delete_artist"),
    path("get_all_my_messages/", get_all_messages, name="get_all_messages"),
    path(
        "handle_change_request/<r_from>/<r_to>/<artist_id>",
        handle_change_request,
        name="handle_artist_change_request",
    ),
    path(
        "<artist_id>/file/<file_id>/delete/",
        delete_artist_file,
        name="delete_artist_file",
    ),
    path(
        "<artist_id>/delete_user_can_change/<user_id>/",
        delete_user_from_changeble,
        name="delete_user_from_changeble",
    ),
    # add permission to change
    path(
        "artist_permission/",
        add_user_permission_to_change_or_see,
        name="add_user_permission_to_change_or_see",
    ),
    path(
        "artist_permission/<artist_id>/<user_phone>/<perm_type>/",
        add_user_permission_to_change_or_see,
        name="add_user_permission_to_change_or_see_double",
    ),
    # change permission to change
    path(
        "artist_permission_change/",
        change_user_permission_to_change_or_see,
        name="change_user_permission_to_change_or_see",
    ),
    path(
        "artist_permission_change/<access_id>/<perm_type>/",
        change_user_permission_to_change_or_see,
        name="change_user_permission_to_change_or_see",
    ),
    # load hechnical and hospitality riders
    path("<artist_id>/technical_raider/", load_tech_rider, name="load_tech_rider"),
    path("<artist_id>/hospitality_raider/", load_hosp_rider, name="load_hosp_rider"),
    path("invite_user/", invite_user, name="invite_user"),
    path("invite_user/<artist_id>/<user_email>/", invite_user, name="invite_user"),
    # contracts
    path(
        "<artist_id>/all_contracts/<date>/",
        get_artist_contracts,
        name="get_artist_contracts",
    ),
    path(
        "<artist_id>/hiden_contracts/",
        get_hiden_artist_contracts,
        name="get_hiden_artist_contracts",
    ),
    path(
        "<contract_id>/hide_contract/<date>/",
        hide_artist_contract,
        name="hide_artist_contract",
    ),
    path(
        "<contract_id>/unhide_contract/",
        unhide_artist_contract,
        name="unhide_artist_contract",
    ),
    path("index/", index),
]
