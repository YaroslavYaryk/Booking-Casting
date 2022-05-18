from django.urls import include, path

from admin_app.admin_artist import urls as artist_urls
from admin_app.admin_company import urls as company_urls
from admin_app.admin_contract import urls as contract_urls
from admin_app.admin_customer import urls as customer_urls
from admin_app.admin_event import urls as event_urls
from admin_app.admin_user import urls as users_admin
from admin_app.admin_venue import urls as venue_urls

from .views import index

urlpatterns = [
    path("", index, name="admin_dashboard"),
    path("artist/", include(artist_urls)),
    path("customer/", include(customer_urls)),
    path("company/", include(company_urls)),
    path("event/", include(event_urls)),
    path("venue/", include(venue_urls)),
    path("contract/", include(contract_urls)),
    path("users/", include(users_admin))
    
]
