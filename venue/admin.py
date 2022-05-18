from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Venue)
admin.site.register(VenueAccess)
admin.site.register(VenueContacts)
admin.site.register(VenueRequestsStorage)
admin.site.register(VenuePictures)

