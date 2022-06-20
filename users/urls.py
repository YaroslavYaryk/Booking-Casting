from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.urls import path, include

from .views import (
    LoginUser,
    LogoutUser,
    RegisterUser,
    add_ability,
    change_password,
    delete_ability,
    load_blocked_page,
    update_view,
    user_profile_view,
)

from .api import urls as users_api

urlpatterns = [
    path("api/", include(users_api)),
    path("login/", LoginUser.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("update_data/", update_view, name="update_user_data"),
    path("change_password/", change_password, name="change_password"),
    path("logout/<slug:admin_name>", LogoutUser.as_view(), name="logout"),
    path("<user_id>/profile/", user_profile_view, name="user_profile_view"),
    path("add_ability/<ability_value>", add_ability, name="add_ability"),
    path("add_ability/", add_ability, name="add_ability"),
    path("delete_ability/<ability_id>", delete_ability, name="delete_ability"),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="reset_password",
    ),
    path(
        "accounts/password_reset_sent/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "accounts/password_change/",
        PasswordChangeView.as_view(
            template_name="registration/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "accounts/password_change/done/",
        PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("page_blocked/", load_blocked_page, name="page_blocked"),
]
