from django.contrib import admin
from .models import (
    Contract,
    ContractTimeClock,
    ContractEventRentalProducts,
    ContractEventTeam,
    ContractRentalProducts,
    TimeClock,
    ArtistTeamEvent,
    CRentalProduct,
    CompanyContractRentalProduct,
    CompanyRentalProduct,
    RentalProductImage,
    CompanyContractOneProduct,
)

# Register your models here.

admin.site.register(Contract)
admin.site.register(ContractTimeClock)
# admin.site.register(ContractEventRentalProducts)
admin.site.register(ContractEventTeam)
# admin.site.register(ContractRentalProducts)
admin.site.register(TimeClock)
admin.site.register(ArtistTeamEvent)
admin.site.register(CRentalProduct)
admin.site.register(CompanyContractRentalProduct)
admin.site.register(CompanyRentalProduct)
admin.site.register(RentalProductImage)
admin.site.register(CompanyContractOneProduct)
