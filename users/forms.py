
from django import forms
from django.conf import settings
from django.contrib.auth.forms import (AuthenticationForm,
                                       ReadOnlyPasswordHashField,
                                       UserCreationForm)

from .models import User


class RegisterUserForm(UserCreationForm):
    """ Registrating form class """

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User

        fields = ("first_name", "last_name",
                  "email", "password1", "password2",)
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'First name'}),
            "last_name": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Last name'}),
            "email": forms.EmailInput(attrs={"class": "form-control", 'placeholder': 'Email address'}),
        }


class LoginUserForm(AuthenticationForm):
    """ Login form class """
    pass

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': 'Password' }))
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Email address'}))

    class Meta:
        model = User

        fields = (
                  "email", "password")



class ChangeForm(forms.ModelForm):
    
    birthdate = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', "phone", "driver_licens_classes", 'picture', "birthdate")
