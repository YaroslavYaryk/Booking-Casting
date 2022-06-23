from django.urls import path

from .views import (
    CompanyListView,
    add_new_company,
    change_company_details,
    delete_company,
    get_all_company_events,
    get_company_details,
    load_company_terms,
    get_company_contracts,
    get_company_hiden_contracts,
    hide_artist_contract,
    unhide_artist_contract,
    change_user_permission_to_change_or_see_company,
    delete_user_from_changeble,
    get_company_provided_products,
    add_company_product,
)

urlpatterns = [
    path("", CompanyListView.as_view(), name="get_my_companies"),
    path("add_new/", add_new_company, name="add_new_company"),
    path("<company_id>/details/", get_company_details, name="get_company_details"),
    path("<company_id>/update/", change_company_details, name="change_company_details"),
    path(
        "<company_id>/delete_company/", delete_company, name="completely_delete_company"
    ),
    # company events
    path(
        "<company_id>/all_events/",
        get_all_company_events,
        name="get_all_company_events",
    ),
    # load category terms
    path("<company_id>/load_terms/", load_company_terms, name="load_company_terms"),
    # contracts
    path(
        "<company_id>/visible_contracts/<date>/",
        get_company_contracts,
        name="get_company_contracts",
    ),
    path(
        "<company_id>/hiden_contracts/",
        get_company_hiden_contracts,
        name="get_company_hiden_contracts",
    ),
    path(
        "<contract_id>/hide_contract_company/<date>/",
        hide_artist_contract,
        name="hide_artist_company_contract",
    ),
    path(
        "<contract_id>/unhide_contract_company/",
        unhide_artist_contract,
        name="unhide_artist_company_contract",
    ),
    # company access
    path(
        "change_user_permission/",
        change_user_permission_to_change_or_see_company,
        name="change_user_permission_to_change_or_see_company",
    ),
    path(
        "change_user_permission/<access_id>/<perm_type>/",
        change_user_permission_to_change_or_see_company,
    ),
    path(
        "company/delete_user_from_changeble/<access_id>/",
        delete_user_from_changeble,
        name="delete_user_from_changeble_company",
    ),
    path(
        "<company_id>/company_products/",
        get_company_provided_products,
        name="get_company_provided_products",
    ),
    path(
        "<company_id>/add_company_product/",
        add_company_product,
        name="add_company_product",
    ),
]
