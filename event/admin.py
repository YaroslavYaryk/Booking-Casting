from django.contrib import admin

from .models import (Event, EventArtists, EventRentalProducts, EventTeam,
                     RentalProducts)

# Register your models here.

admin.site.register(Event)
admin.site.register(EventArtists)
admin.site.register(EventTeam)
admin.site.register(EventRentalProducts)
admin.site.register(RentalProducts)
