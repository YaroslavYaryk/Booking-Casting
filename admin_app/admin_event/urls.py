from django.urls import include, path

from .views import (EventArtistsListView, EventRentalProductsView,
                    EventTeamListView, MyEventsListView, RentalProductsView,
                    add_new_event, add_new_event_artist,
                    add_new_event_rental_product, add_new_event_team,
                    add_new_rental_product, admin_delete_event_artist,
                    admin_delete_event_product, admin_delete_event_team,
                    admin_delete_rental_product, change_details_event_team,
                    change_event_artist, change_event_product,
                    change_rental_product, delete_event, update_event)

urlpatterns = [
    # event
    path("all_events/", MyEventsListView.as_view(), name="admin_get_all_eevents"),
    path("add_new_event/", add_new_event, name='admin_add_new_event'),
    path("<event_id>/update_event/", update_event, name="admin_update_event"),
    path("<event_id>/delete_event/", delete_event, name="admin_delete_event"),
    
    # event team
    path("all_event_teams/", EventTeamListView.as_view(), name="admin_get_all_event_teams"),
    path("add_new_event_team/", add_new_event_team, name="admin_add_new_event_team"),
    path("<event_team_id>/update_event_team/", change_details_event_team, name="admin_change_details_event_team"),
    path("<event_team_id>/delete_event_team/", admin_delete_event_team, name="admin_admin_delete_event_team"),
    
    # event artists
    path("all_eveent_artists/", EventArtistsListView.as_view(), name="admin_get_all_events_artists"),
    path("add_new_event_artist/", add_new_event_artist, name="admin_add_new_event_artist"),
    path("<event_artist_id>/update_event_artist/", change_event_artist, name="admin_change_event_artist"),
    path("<event_artist_id>/delete_event_artist/", admin_delete_event_artist, name="admin_delete_event_artist"),
    
    # rental products
    path("all_rental_products/", RentalProductsView.as_view(), name="admin_get_all_rental_products"),
    path("add_new_rental_product/", add_new_rental_product, name="admin_add_new_rental_product"),
    path("<rental_product_id>/update_rental_product/", change_rental_product, name="admin_change_rental_product"),
    path("<rental_product_id>/delete_rental_product/", admin_delete_rental_product, name="admin_delete_rental_product"),
    
    # event rental products
    path("all_event_rental_products/", EventRentalProductsView.as_view(), name="admin_get_all_event_rental_products"),
    path("add_new_event_product/", add_new_event_rental_product, name="add_new_event_rental_product"),
    path("<event_product_id>/update_event_product/", change_event_product, name="admin_change_event_product"),
    path("<event_product_id>/delete_event_product/", admin_delete_event_product, name="admin_admin_delete_event_product")
    
]
