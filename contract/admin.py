from django.contrib import admin
from .models import (
    Contract,
    ContractTimeClock,
    ContractEventRentalProducts,
    ContractEventTeam,
    ContractRentalProducts,
)

# Register your models here.

admin.site.register(Contract)
admin.site.register(ContractTimeClock)
admin.site.register(ContractEventRentalProducts)
admin.site.register(ContractEventTeam)
admin.site.register(ContractRentalProducts)
