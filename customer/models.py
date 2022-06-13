from django.db import models
from users.models import User


# Create your models here.
class Customer(models.Model):
    """class of single product"""

    organization_number = models.CharField(
        "Organization number", max_length=255, unique=True
    )
    name = models.CharField("Name", max_length=255, unique=True)
    address = models.CharField("Address", max_length=255)
    zip_code = models.CharField("Zip Code", max_length=255)

    city = models.CharField("City", max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        return self.active


class CustomerContacts(models.Model):
    """class of single product"""

    customer = models.ForeignKey(
        Customer, verbose_name=("customer"), on_delete=models.CASCADE
    )
    first_name = models.CharField("first name", max_length=255)
    last_name = models.CharField("last name", max_length=255)
    phone = models.CharField("phone", max_length=255)
    email = models.EmailField("email", max_length=255)
    role = models.CharField("role", max_length=255)
    birthdate = models.CharField("birth date", max_length=255)
    signatory_rights = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.customer.name

    @property
    def is_active(self):
        return self.active


class CustomerAccess(models.Model):
    """class of single product"""

    customer = models.ForeignKey(
        Customer, verbose_name="customer_access", on_delete=models.CASCADE
    )
    access = models.ForeignKey(
        User, verbose_name=("access"), on_delete=models.CASCADE, null=True
    )
    admin = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "customer",
            "access",
        )

    def __str__(self):
        return self.customer.name

    @property
    def is_admin(self):
        return self.admin


class CustomerRequestsStorage(models.Model):
    # Create your models here.
    """class of train route"""

    requester = models.ForeignKey(
        User,
        verbose_name=("requester name"),
        on_delete=models.CASCADE,
        related_name="customer_requester",
    )
    owner = models.ForeignKey(
        User,
        verbose_name=("owner"),
        on_delete=models.CASCADE,
        related_name="customer_owner",
    )

    customer = models.ForeignKey(
        Customer, verbose_name="customer_on_request_storage", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now=True)
    granted = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "requester",
            "owner",
            "customer",
        )

    def __str__(self):
        return f"{self.requester} + {self.owner} + {self.customer}"


class CustomerNonUserEdit(models.Model):
    # Create your models here.
    """class of train route"""

    customer = models.ForeignKey(
        Customer, verbose_name=("Customer"), on_delete=models.CASCADE
    )
    user_email = models.CharField(("User Email"), max_length=100)

    class Meta:
        unique_together = (
            "customer",
            "user_email",
        )

    def __str__(self):
        return f"{self.customer.name} - {self.user_email}"
