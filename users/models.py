from datetime import date

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import DateTimeField


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Bruker må ha en e-postadresse")
        if not password:
            raise ValueError("Bruker må ha et passord")
        if not first_name:
            raise ValueError("Bruker må ha et fornavn")
        if not last_name:
            raise ValueError("Bruker må ha et etternavn")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="images/users", blank=True)
    phone = models.CharField(max_length=50, blank=True)
    driver_licens_classes = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # can login
    admin = models.BooleanField(default=False)  # can login

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.birthdate and self.birthdate > date.today():
            raise ValidationError("The date cannot be in the future!")
        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        full_name = self.first_name.title() + " " + self.last_name.title()
        return full_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def full_name(self):
        full_name = self.first_name.title() + " " + self.last_name.title()
        return full_name


class UserAbilities(models.Model):

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    ability = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.ability}"

    class Meta:

        """our model display in django-admin"""

        verbose_name = "User Abilitie"
        verbose_name_plural = "User Abilities"
        ordering = ["id"]  # sorting categories at site
