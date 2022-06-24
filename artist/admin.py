from django.contrib import admin

from .models import (
    Artist,
    ArtistAccess,
    ArtistAssets,
    ArtistFile,
    ArtistRequestsStorage,
    ArtistUserStatus,
    ArtistBusyDates,
)

# Register your models here.
admin.site.register(Artist)
admin.site.register(ArtistAccess)
admin.site.register(ArtistAssets)
admin.site.register(ArtistRequestsStorage)
admin.site.register(ArtistFile)
admin.site.register(ArtistUserStatus)
admin.site.register(ArtistBusyDates)
