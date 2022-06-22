from django.contrib import admin

from .models import Company, CompanyAccess

# Register your models here.
admin.site.register(Company)
admin.site.register(CompanyAccess)
