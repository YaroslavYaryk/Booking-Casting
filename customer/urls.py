from django.urls import path

from .views import (
    CustomerListView,
    MyCustomerListView,
    add_new_customer,
    add_user_permission_to_change_or_see_customer,
    change_details_customer,
    change_user_permission_to_change_or_see_customer,
    delete_customer,
    delete_user_from_customer_changeble,
    get_customer_details,
    handle_change_request,
    send_request_to_change_customer,
    invite_user,
    get_customer_details_for_non_user,
    change_details_customer_non_user,
    delete_non_user_from_editing,
)

urlpatterns = [
    path("all/", CustomerListView.as_view(), name="all_customers"),
    path("my/", MyCustomerListView.as_view(), name="my_customers"),
    path("add_new/", add_new_customer, name="add_new_customer"),
    path("<customer_id>/details/", get_customer_details, name="customer_details"),
    path(
        "<customer_id>/details_non_user/<non_user_id>/",
        get_customer_details_for_non_user,
        name="get_customer_details_for_non_user",
    ),
    path(
        "<customer_id>/update/", change_details_customer, name="change_details_customer"
    ),
    path(
        "<customer_id>/update_non_user/<non_user_id>/",
        change_details_customer_non_user,
        name="change_details_customer_non_user",
    ),
    path("<customer_id>/delete/", delete_customer, name="delete_customer"),
    path(
        "<customer_id>/delete_non_user_editable/<non_user_id>/",
        delete_non_user_from_editing,
        name="delete_non_user_from_editing",
    ),
    path(
        "send_request_to_change_customer/<customer_id>/",
        send_request_to_change_customer,
        name="send_request_to_change_customer",
    ),
    path(
        "handle_change_request/<r_from>/<r_to>/<customer_id>",
        handle_change_request,
        name="handle_customer_change_request",
    ),
    path(
        "<customer_id>/delete_user_can_change/<user_id>/",
        delete_user_from_customer_changeble,
        name="delete_user_from_customer_changeble",
    ),
    # add permission to change
    path(
        "customer_permission/",
        add_user_permission_to_change_or_see_customer,
        name="add_user_permission_to_change_or_see_customer",
    ),
    path(
        "customer_permission/<customer_id>/<user_phone>/<perm_type>/",
        add_user_permission_to_change_or_see_customer,
        name="add_user_permission_to_change_or_see_customer",
    ),
    # change permission to change
    path(
        "customer_permission_change/",
        change_user_permission_to_change_or_see_customer,
        name="change_user_permission_to_change_or_see_customer",
    ),
    path(
        "customer_permission_change/<access_id>/<perm_type>/",
        change_user_permission_to_change_or_see_customer,
        name="change_user_permission_to_change_or_see_customer",
    ),
    # invite user
    path("invite_user/", invite_user, name="customer_invite_user"),
    path(
        "invite_user/<customer_id>/<user_email>/",
        invite_user,
        name="customer_invite_user",
    ),
]
