from django.urls import path

from .views import (MyEventsListView, add_event_product, add_new_event,
                    add_user_to_team, delete_artist_from_event, delete_event,
                    delete_event_product, delete_user_from_team,
                    edit_event_artist, edit_event_product, edit_user_in_team,
                    get_event_artist_list, get_event_details,
                    get_event_products_list, load_contract_for_event,
                    update_event, get_contract)

urlpatterns = [
    path("list/", MyEventsListView.as_view(), name="get_all_events"),
    path("add_new/", add_new_event, name="add_new_event"),
    path("<event_id>/details", get_event_details, name="get_event_details"),
    path("<event_id>/update/", update_event, name="update_event"),
    path("<event_id>/delete/", delete_event, name="delete_event"),
    path("<event_id>/contract/", load_contract_for_event, name="load_contract_for_event"),
    path("<event_id>/artists/", get_event_artist_list, name="get_event_artist_list"),
    path("<event_id>/delete_artist/<artist_id>/", delete_artist_from_event, name="delete_artist_from_event"),
    path("<event_id>/edit_artist/<ev_artist_id>/", edit_event_artist, name="edit_event_artist"),
    
    path("<event_id>/add_user_to_team/", add_user_to_team, name="add_user_to_team"),
    path("edit_user_in_team/", edit_user_in_team, name="edit_user_in_team"),
    path("edit_user_in_team/<event_id>/<user_email>/<role>/", edit_user_in_team, name="edit_user_in_team_full"),
    path("<event_id>/delete_user_from_team/<user_email>/", delete_user_from_team, name="delete_user_from_team"),
    
    path("<event_id>/add_event_product/", add_event_product, name="add_event_product"),
    
    # event products
    path("<event_id>/products_list/", get_event_products_list, name="get_event_products_list"),
    path("<event_id>/delete_event_product/<product_id>/", delete_event_product, name="delete_event_product"),
    path("<event_id>/edit_event_product/<product_id>/", edit_event_product, name="edit_event_product"),
    path("<event_artist_id>/sign_contract/", get_contract, name="sign_contract")

    
]
