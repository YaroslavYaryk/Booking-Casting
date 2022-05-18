from django.urls import include, path

from .views import (UserAbilitiesListView, UserListView, add_new_user,
                    add_new_user_ability, admin_change_user_password,
                    admin_delete_user, admin_delete_user_ability,
                    change_details_user, change_details_user_abilities)

urlpatterns = [
    # users
    path("all_users/", UserListView.as_view(), name="admin_get_all_users"),
    path("add_user/", add_new_user, name="admin_add_new_user"),
    path("<user_id>/update_user/", change_details_user, name="admin_change_details_user"),
    path("<user_id>/delete_user", admin_delete_user, name="admin_delete_user"),
    
    path("<user_id>/admin_change_password", admin_change_user_password, name="admin_change_user_password"),
    
    # user abilities
    path("all_abilities/", UserAbilitiesListView.as_view(), name="admin_get_all_user_abilities"),
    path("add_user_ability/", add_new_user_ability, name="admin_add_new_user_ability"),
    path("<ability_id>/update_user_ability/", change_details_user_abilities, name="admin_change_details_user_abilities"),
    path("<ability_id>/delete_user_ability", admin_delete_user_ability, name="admin_admin_delete_user_ability"),
]
