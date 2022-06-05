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
]
