from datetime import date
from re import T

from artist.models import Artist
from ckeditor.fields import RichTextField
from company.models import Company
from customer.models import Customer
from django.core.exceptions import ValidationError
from django.db import models
from multiselectfield import MultiSelectField
from users.models import User
from venue.models import Venue


# Create your models here.
class Event(models.Model):

    name = models.CharField("Name", max_length=255)
    date = models.DateField("Date")
    opening = models.TimeField(("Opening Time"), auto_now=False, auto_now_add=False)
    closing = models.TimeField(("Closing Time"), auto_now=False, auto_now_add=False)
    venue = models.ForeignKey(Venue, verbose_name=("Venue"), on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, verbose_name=("Customer"), on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name=("Company"), on_delete=models.CASCADE)
    contract_template = RichTextField(null=True)
    contract = RichTextField(blank=True)
    
    def save(self, *args, **kwargs):
        if self.date and  self.date < date.today():
            raise ValidationError("The date cannot be in the past!")
        super(Event, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name



class EventTeam(models.Model):
    """ class of single product """

    event = models.ForeignKey(Event, verbose_name=("Event"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=("Event User"), on_delete=models.CASCADE)
    role = models.CharField("role", max_length=255)
    
    class Meta:
        unique_together = ('event', 'user',)
    
    
    def __str__(self):
        return self.event.name




class EventArtists(models.Model):
    """ class of single product """

    event = models.ForeignKey(Event, verbose_name="event_artists", on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, verbose_name=("Event artist"), on_delete=models.CASCADE, null=True)
    show_duration = models.CharField("Show Duration", max_length=255)
    price = models.IntegerField(("Price"))
    
    POWER_CHOICES =(
        ("Reise", "Reise"),
        ("Opphold", "Opphold"),
        ("Kost", "Kost"),
        ("Interntransport", "Interntransport"),
        ("Tono", "Tono"),
        ("Technicalraider", "Technicalraider"),
        ("Hospitalityrider", "Hospitalityrider"),
    )
    
    customers_responsibility = MultiSelectField(choices=POWER_CHOICES)
    
    class Meta:
        unique_together = ('event', 'artist',)


    def __str__(self):
        return self.event.name


class RentalProducts(models.Model):
    
    name = models.CharField(("Product name"), max_length=150)
    picture = models.FileField(("Picture"), upload_to="event_rental_products/")

    def __str__(self) :
        return  self.name


class EventRentalProducts(models.Model):
    
    event = models.ForeignKey(Event, verbose_name="event_artists", on_delete=models.CASCADE)
    rental_products = models.ForeignKey(RentalProducts, verbose_name="event_rental_products", on_delete=models.CASCADE)
    price = models.IntegerField(("Price"))
    count = models.IntegerField(("Count"))
    
    class Meta:
        unique_together = ('event', 'rental_products',)
    

    def __str__(self) :
        return  self.event.name

