"""booking_casting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from artist.views import index as ind
from users.views import index
from django.utils.translation import gettext_lazy as _

urlpatterns = (
    [
        path(_("admin/"), admin.site.urls),
        # path("i18n/", include("django.conf.urls.i18n")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + i18n_patterns(
        # path("i/", ind, name="ind"),
        path("users/", include("users.urls")),
        path("artist/", include("artist.urls")),
        path("company/", include("company.urls")),
        path("contract/", include("contract.urls")),
        path("customer/", include("customer.urls")),
        path("event/", include("event.urls")),
        path("venue/", include("venue.urls")),
        path("admin_site/", include("admin_app.urls")),
        path("", index, name="home"),
        path("ckeditor/", include("ckeditor_uploader.urls")),
        path("api-auth/", include("rest_framework.urls")),
    )
)


handler403 = "users.views.handler_forbiden"
