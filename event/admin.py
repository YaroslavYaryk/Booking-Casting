from django.contrib import admin

from .models import Event, EventRentalProducts, EventTeam, RentalProducts

# Register your models here.

admin.site.register(Event)
admin.site.register(EventTeam)
admin.site.register(EventRentalProducts)
admin.site.register(RentalProducts)
