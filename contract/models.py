from datetime import date
from django.db import models
from django.forms import ValidationError
from pkg_resources import require
from artist.models import Artist
from ckeditor.fields import RichTextField
from company.models import Company
from customer.models import Customer
from venue.models import Venue
from multiselectfield import MultiSelectField


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
