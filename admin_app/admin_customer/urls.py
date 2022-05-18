from django.urls import include, path

from .views import (CustomerAccesstListView, CustomerContactsListView,
                    CustomerListView, CustomerRequestStorageListView,
                    add_new_customer, add_new_customer_access,
                    add_new_customer_contacts,
                    add_new_customer_request_storage,
                    admin_delete_customer_access,
                    admin_delete_customer_request_storage,
                    change_details_customer, change_details_customer_access,
                    change_details_customer_contacts,
                    change_details_customer_request_storage, delete_customer,
                    delete_customer_contacts)

urlpatterns = [
    # customer
    path("all_customers/", CustomerListView.as_view(), name="admin_get_all_customers"),
    path("add_customer/", add_new_customer, name = 'admin_add_new_customer'),
    path("<customer_id>/update_customer/", change_details_customer, name="admin_change_details_customer"),
    path("<customer_id>/delete_customer", delete_customer, name = "admin_delete_customer"),
    
    # customer contacts
    path("all_customer_contacts", CustomerContactsListView.as_view(), name = "admin_get_all_customer_contacts"),
    path("add_customer_contacts/", add_new_customer_contacts, name="admin_add_new_customer_contacts"),
    path("<customer_contacts_id>/update_contacts/", change_details_customer_contacts, name="admin_change_details_customer_contacts"),
    path("<customer_contacts_id>/delete_contacts/", delete_customer_contacts, name="admin_delete_customer_contacts"),
    
    # customer access 
    path("all_customer_access/", CustomerAccesstListView.as_view(), name="admin_get_all_customer_access"),
    path("add_new_customer_access/", add_new_customer_access, name="admin_add_new_customer_access"),
    path("<access_id>/change_details_customer_access/", change_details_customer_access, name="admin_change_details_customer_access"),
    path("<access_id>/delete_customer_access/", admin_delete_customer_access, name="admin_delete_customer_access"),
    
    # customer request storage
    path("all_customer_requests/", CustomerRequestStorageListView.as_view(), name="admin_get_all_customer_requests"),
    path("add_new_customer_request_storage/", add_new_customer_request_storage, name="admin_add_new_customer_request_storage"),
    path("<request_storage_id>/change_details/", change_details_customer_request_storage, name="admin_change_details_customer_request_storage"),
    path("<request_storage_id>/delete_request/", admin_delete_customer_request_storage, name="admin_delete_customer_request_storage")
]
