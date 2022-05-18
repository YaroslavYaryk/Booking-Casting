from django.urls import include, path

from .views import (VenueAccesstListView, VenueContactsListView, VenueListView,
                    VenuePicturesListView, VenueRequestStorageListView,
                    add_new_venue, add_new_venue_access,
                    add_new_venue_contacts, add_new_venue_picture,
                    add_new_venue_request_storage, admin_delete_venue_access,
                    admin_delete_venue_picture,
                    admin_delete_venue_request_storage, change_details_venue,
                    change_details_venue_access, change_details_venue_contacts,
                    change_details_venue_picture,
                    change_details_venue_request_storage, delete_venue,
                    delete_venue_contacts)

urlpatterns = [
    # venue
    path("all_venues/", VenueListView.as_view(), name="admin_get_all_venues"),
    path("add_venue/", add_new_venue, name = 'admin_add_new_venue'),
    path("<venue_id>/update_venue/", change_details_venue, name="admin_change_details_venue"),
    path("<venue_id>/delete_venue", delete_venue, name = "admin_delete_venue"),
    
    # # venuecontacts
    path("all_venue_contacts", VenueContactsListView.as_view(), name = "admin_get_all_venue_contacts"),
    path("add_venue_contacts/", add_new_venue_contacts, name="admin_add_new_venue_contacts"),
    path("<venue_contacts_id>/update_contacts/", change_details_venue_contacts, name="admin_change_details_venue_contacts"),
    path("<venue_contacts_id>/delete_contacts/", delete_venue_contacts, name="admin_delete_venue_contacts"),
    
    # # venue access 
    path("all_venue_access/", VenueAccesstListView.as_view(), name="admin_get_all_venue_access"),
    path("add_new_venue_access/", add_new_venue_access, name="admin_add_new_venue_access"),
    path("<access_id>/change_details_venue_access/", change_details_venue_access, name="admin_change_details_venue_access"),
    path("<access_id>/delete_venue_access/", admin_delete_venue_access, name="admin_delete_venue_access"),
    
    # # venue request storage
    path("all_venue_requests/", VenueRequestStorageListView.as_view(), name="admin_get_all_venue_requests"),
    path("add_new_venue_request_storage/", add_new_venue_request_storage, name="admin_add_new_venue_request_storage"),
    path("<request_storage_id>/change_details/", change_details_venue_request_storage, name="admin_change_details_venue_request_storage"),
    path("<request_storage_id>/delete_request/", admin_delete_venue_request_storage, name="admin_delete_venue_request_storage"),
    
     # # venue pictures
    path("all_venue_pictures/", VenuePicturesListView.as_view(), name="admin_get_all_venue_pictures"),
    path("add_new_venue_picture/", add_new_venue_picture, name="admin_add_new_venue_picture"),
    path("<picture_id>/change_details_picture/", change_details_venue_picture, name="admin_change_details_venue_picture"),
    path("<picture_id>/delete_picture/", admin_delete_venue_picture, name="admin_delete_venue_picture")
]
