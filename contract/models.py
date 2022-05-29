from django.db import models
from artist.models import Artist
from ckeditor.fields import RichTextField
from company.models import Company
from customer.models import Customer
from venue.models import Venue


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

    price = models.CharField(("Price"), max_length=255)
    payment_methods = models.TextField(("Payment Methods"), null=True)
    date = models.DateField("Date", null=True)
    comment = models.TextField(("Comment"), blank=True, null=True)
    contract = RichTextField("Artist Contract", null=True, blank=True)
    contract_pdf_url = models.CharField(("Contract PDF"), max_length=150, null=True)

    def __str__(self):
        return self.artist.name
