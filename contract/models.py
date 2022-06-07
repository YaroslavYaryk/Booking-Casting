from datetime import date
from django.db import models
from django.forms import ValidationError
from artist.models import Artist
from ckeditor.fields import RichTextField
from company.models import Company
from customer.models import Customer
from venue.models import Venue
from multiselectfield import MultiSelectField
from users.models import User


class Contract(models.Model):
    """class of single product"""

    artist = models.ForeignKey(
        Artist, verbose_name=("Contract artist"), on_delete=models.CASCADE, null=True
    )
    customer = models.ForeignKey(
        Customer, verbose_name=("Customer"), on_delete=models.CASCADE, null=True
    )
    company = models.ForeignKey(
        Company, verbose_name=("Company"), on_delete=models.CASCADE, null=True
    )
    venue = models.ForeignKey(
        Venue, verbose_name=("Venue"), on_delete=models.CASCADE, null=True
    )

    price = models.FloatField(("Price"), max_length=255)
    payment_methods = models.TextField(("Payment Methods"), null=True)
    date = models.DateField("Date", null=True)
    comment = models.TextField(("Comment"), blank=True, null=True)
    visible = models.BooleanField(("Visible"), default=True, null=True)
    signed = models.BooleanField(("Signed"), default=False, null=True)

    ADITIONAL_STAFF_CHOICES = (
        ("Reise", "Reise"),
        ("Hotell", "Hotell"),
        ("Tono", "Tono"),
        ("Interntransport", "Interntransport"),
        ("Middag", "Middag"),
        ("Lunsj", "Lunsj"),
        ("Teknikk", "Teknikk"),
    )
    aditional_staff = MultiSelectField(choices=ADITIONAL_STAFF_CHOICES, null=True)

    contract = RichTextField("Artist Contract", null=True, blank=True)
    contract_pdf_url = models.CharField(
        ("Contract PDF"), max_length=150, null=True, blank=True
    )

    class Meta:
        unique_together = (
            "artist",
            "customer",
        )

    def __str__(self):
        return self.artist.name


class ContractEventTeam(models.Model):
    """class of single product"""

    contract = models.ForeignKey(
        Contract, verbose_name=("Event"), on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, verbose_name=("Event User"), on_delete=models.CASCADE
    )
    role = models.CharField("role", max_length=255)

    class Meta:
        unique_together = (
            "contract",
            "user",
        )

    def __str__(self):
        return f"{self.contract.artist} - {self.contract.customer}"


class ContractRentalProducts(models.Model):

    name = models.CharField(("Product name"), max_length=150)
    picture = models.FileField(("Picture"), upload_to="event_rental_products/")

    def __str__(self):
        return self.name


class ContractEventRentalProducts(models.Model):

    contract = models.ForeignKey(
        Contract, verbose_name="event_artists", on_delete=models.CASCADE
    )
    rental_products = models.ForeignKey(
        ContractRentalProducts,
        verbose_name="event_rental_products",
        on_delete=models.CASCADE,
    )
    price = models.IntegerField(("Price"))
    count = models.IntegerField(("Count"))

    class Meta:
        unique_together = (
            "contract",
            "rental_products",
        )

    def __str__(self):
        return f"{self.contract.artist.name} - { self.contract.customer.name}"


class TimeClock(models.Model):

    start_time = models.TimeField(
        ("Action Start Tume"), auto_now=False, auto_now_add=False
    )
    end_time = models.TimeField(("Action End Tume"), auto_now=False, auto_now_add=False)
    action = models.CharField(("Action"), max_length=100)

    def __str__(self):
        return f"{self.start_time} - {self.end_time} - {self.action}"


class ContractTimeClock(models.Model):

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    day_schedule = models.ManyToManyField(TimeClock, verbose_name=("Day Schedule"))

    def __str__(self):
        return f"{self.contract.artist} - {self.contract.customer}"
