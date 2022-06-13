import imp

from django.contrib import admin

from .models import (
    Customer,
    CustomerAccess,
    CustomerContacts,
    CustomerRequestsStorage,
    CustomerNonUserEdit,
)

# Register your models here.


admin.site.register(Customer)
admin.site.register(CustomerContacts)
admin.site.register(CustomerRequestsStorage)
admin.site.register(CustomerAccess)
admin.site.register(CustomerNonUserEdit)
