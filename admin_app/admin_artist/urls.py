from django.urls import path

from .views import (ArtisAccesstListView, ArtistAssetsListView,
                    ArtistFilesListView, ArtistListView,
                    ArtistRequestStorageListView, add_new_artist,
                    add_new_artist_access, add_new_artist_assets,
                    add_new_artist_file, add_new_artist_request_storage,
                    admin_delete_artist_access, admin_delete_artist_assets,
                    admin_delete_artist_file,
                    admin_delete_artist_request_storage, change_details_artist,
                    change_details_artist_access, change_details_artist_assets,
                    change_details_artist_file,
                    change_details_artist_request_storage, delete_artist)

urlpatterns = [
    # artist
    path("all_artists/", ArtistListView.as_view(), name="admin_get_all_artist"),
    path("add_artist/", add_new_artist, name="admin_add_new_artist"),
    path("<artist_id>/ update_artist/", change_details_artist, name="admin_change_details_artist"),
    path("<artist_id>/delete_artist/", delete_artist, name="admin_delete_artist"),
    
    # artist access
    path("all_access/", ArtisAccesstListView.as_view(), name = "admin_get_all_artist_access"),
    path("add_access/", add_new_artist_access, name="admin_add_new_artist_access"),
    path("<access_id>/update_access/", change_details_artist_access, name="admin_change_details_artist_access"),
    path("<access_id>/delete_access/", admin_delete_artist_access, name="admin_delete_artist_access"),
    
    #files
    path("all_files/", ArtistFilesListView.as_view(), name="admin_get_all_files"),
    path("add_file", add_new_artist_file, name="admin_add_new_artist_file"),
    path("<file_id>/update_file/", change_details_artist_file, name="admin_change_details_artist_file"),
    path("<file_id>/delete_file", admin_delete_artist_file, name="admin_delete_artist_file"),
    
    # artist assets
    path("all_assets/", ArtistAssetsListView.as_view(), name="admin_get_all_artist_assets"),
    path("add_assets", add_new_artist_assets, name = "admin_add_new_artist_assets"),
    path("<assets_id>/update_assets/", change_details_artist_assets, name="admin_change_details_artist_assets"),
    path("<assets_id>/delete/", admin_delete_artist_assets, name="admin_admin_delete_artist_assets"),
    
    # artist request storage
    path("all_request_storage/", ArtistRequestStorageListView.as_view(), name="admin_get_all_request_storage"),
    path("add_request_storage/", add_new_artist_request_storage, name="admin_add_new_artist_request_storage"),
    path("<request_storage_id>/update_request_storage/", change_details_artist_request_storage, name="admin_change_details_artist_request_storage"),
    path("<request_storage_id>/delete_request_storage/", admin_delete_artist_request_storage, name="admin_delete_artist_request_storage")
    
]
