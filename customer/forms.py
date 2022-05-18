from django import forms

from .models import Customer, CustomerContacts


class CustomerAddForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ("name", "address", "zip_code", "city", "active" )


class CustomerContactsAddForm(forms.ModelForm):
    
    class Meta:
        model = CustomerContacts
        exclude = ("customer",)
