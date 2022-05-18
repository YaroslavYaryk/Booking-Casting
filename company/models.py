from django.db import models
from users.models import User


# Create your models here.
class Company(models.Model):
    
    organization_number = models.CharField(("Organozation Number"), max_length=150)
    name = models.CharField(("Name"), max_length=150)
    address = models.CharField(("Address"), max_length=150)
    zip_code = models.CharField(("Zip Code"), max_length=50) 
    city = models.CharField(("City"), max_length=50)
    active = models.BooleanField(("Active"), default=True)
    creator = models.ForeignKey(User, verbose_name=("creator"), related_name="company_creator", on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name
    
    @property
    def is_active(self):
        return self.active
