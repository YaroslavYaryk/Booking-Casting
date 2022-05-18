from django.urls import include, path

from .views import (CompanyListView, add_new_company, change_details_company,
                    delete_company)

urlpatterns = [
    path("all_companies/", CompanyListView.as_view(), name="admin_get_all_companies"),
    path("add_company/", add_new_company, name="admin_add_new_company"),
    path("<company_id>/update/", change_details_company, name="change_details_company"),
    path("<company_id>/delete_company", delete_company, name="admin_delete_company")
]
