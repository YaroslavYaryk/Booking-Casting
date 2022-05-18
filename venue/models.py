from django.db import models
from multiselectfield import MultiSelectField
from users.models import User


# Create your models here.
class Venue(models.Model):

    name = models.CharField("Name", max_length=255)
    address = models.CharField("Address", max_length=255)
    zip_code = models.CharField("Zip Code", max_length=255)
    city = models.CharField("City", max_length=255)
    phone = models.CharField("Phone", max_length=255) 
    email = models.EmailField("Email", max_length=255) 
    capacity = models.CharField("Capacity", max_length=255) 
    opening = models.TimeField(("Opening Time"), auto_now=False, auto_now_add=False)
    closing = models.TimeField(("Closing Time"), auto_now=False, auto_now_add=False)
    age_limit = models.IntegerField(("Age Limit"))
    comment = models.TextField(("Comment"))
    equipment = models.TextField(("Equipment"))
    
    POWER_CHOICES =(
        ("32 Amp Blå", "32 Amp Blå"),
        ("32 Amp rød", "32 Amp rød"),
        ("63 Amp Blå", "63 Amp Blå"),
        ("63 Amp rød", "63 Amp rød"),
    )
    power = MultiSelectField(choices=POWER_CHOICES)
    
    active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.name

    @property
    def is_active(self):
        return self.active


class VenueContacts(models.Model):
    """ class of single product """

    venue = models.ForeignKey(Venue, verbose_name=("Venue"), on_delete=models.CASCADE)
    first_name = models.CharField("first name", max_length=255, unique=True)
    last_name = models.CharField("last name", max_length=255)
    phone = models.CharField("phone", max_length=255)
    epost = models.EmailField("email", max_length=255)
    role = models.CharField("role", max_length=255)
    active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.venue.name

    @property
    def is_active(self):
        return self.active


class VenueAccess(models.Model):
    """ class of single product """

    venue = models.ForeignKey(Venue, verbose_name="venue_access", on_delete=models.CASCADE)
    access = models.ForeignKey(User, verbose_name=("access"), on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('venue', 'access',)

    def __str__(self):
        return self.venue.name


    @property
    def is_admin(self):
        return self.admin


class VenueRequestsStorage(models.Model):
    # Create your models here.
    """class of train route"""

    requester = models.ForeignKey(
        User,
        verbose_name=("requester name"),
        on_delete=models.CASCADE,
        related_name="venue_requester",
    )
    owner = models.ForeignKey(
        User,
        verbose_name=("owner"),
        on_delete=models.CASCADE,
        related_name="venue_owner",
    )

    venue = models.ForeignKey(Venue, verbose_name="venue_on_request_storage", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    granted = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    
    
    class Meta:
        unique_together = ('requester', 'owner', "venue",)

    def __str__(self):
        return f"{self.requester} + {self.owner} + {self.venue}"
    


class VenuePictures(models.Model):
    
    venue = models.ForeignKey(Venue, verbose_name="venue_picture", on_delete=models.CASCADE)
    file = models.FileField(("Picture"), upload_to="venue_pictures/")

    def __str__(self) :
        return  self.venue.name
