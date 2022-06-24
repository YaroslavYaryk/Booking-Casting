from ckeditor.fields import RichTextField
from datetime import date
from django.db import models
from users.models import User


# Create your models here.
class Artist(models.Model):
    """class of single product"""

    name = models.CharField("name", max_length=255, unique=True)
    technical_raider = RichTextField("technical raider")
    hospitality_raider = RichTextField("technical raider")
    active = models.BooleanField(default=True)
    date_created = models.DateField(
        "Date created",
    )

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        return self.active


class ArtistAccess(models.Model):
    """class of single product"""

    artist = models.ForeignKey(
        Artist, verbose_name="artist_access", on_delete=models.CASCADE
    )
    access = models.ForeignKey(
        User, verbose_name=("access"), on_delete=models.CASCADE, null=True
    )
    admin = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "artist",
            "access",
        )

    def __str__(self):
        return self.artist.name

    @property
    def is_admin(self):
        return self.admin


class ArtistFile(models.Model):
    """class of single product"""

    name = models.CharField("name", max_length=255, null=True)
    file = models.FileField(upload_to="artist_assets")

    def __str__(self):
        return self.name


class ArtistAssets(models.Model):
    """class of single product"""

    artist = models.ForeignKey(
        Artist, verbose_name="artist_access", on_delete=models.CASCADE
    )
    file = models.ManyToManyField(ArtistFile)
    credit = models.CharField("credit", max_length=255)

    def __str__(self):
        return self.artist.name

    @property
    def is_admin(self):
        return self.admin


class ArtistRequestsStorage(models.Model):
    # Create your models here.
    """class of train route"""

    requester = models.ForeignKey(
        User,
        verbose_name=("requester name"),
        on_delete=models.CASCADE,
        related_name="requester",
    )
    owner = models.ForeignKey(
        User,
        verbose_name=("owner"),
        on_delete=models.CASCADE,
        related_name="owner",
    )

    artist = models.ForeignKey(Artist, verbose_name="artist", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    granted = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "requester",
            "owner",
            "artist",
        )

    def __str__(self):
        return f"{self.requester} + {self.owner} + {self.artist}"


class ArtistUserStatus(models.Model):
    # Create your models here.
    """class of train route"""

    user_access = models.OneToOneField(ArtistAccess, on_delete=models.CASCADE)

    last_asset = models.ForeignKey(
        ArtistAssets,
        verbose_name="artist assets",
        on_delete=models.CASCADE,
        default="none",
    )
    invited = models.BooleanField(("Invited"), null=True)
    last_added_user = models.ForeignKey(
        User, verbose_name=("Last Added User"), on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user_access.artist.name}"


class ArtistBusyDates(models.Model):

    artist = models.ForeignKey(
        Artist, verbose_name=("Artist"), on_delete=models.CASCADE
    )
    start_date = models.DateField("start_date")
    end_date = models.DateField("end_date")
    busy_action = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.artist.name} - {self.start_date} - {self.end_date} - {self.busy_action}"
