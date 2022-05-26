from customer.models import (
    Customer,
    CustomerAccess,
    CustomerContacts,
    CustomerRequestsStorage,
)
from django import forms


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class CustomerContactsForm(forms.ModelForm):
    class Meta:
        model = CustomerContacts
        fields = "__all__"


class CustomerAccessForm(forms.ModelForm):
    class Meta:
        model = CustomerAccess
        fields = "__all__"


class CustomerRequestStorageForm(forms.ModelForm):
    class Meta:
        model = CustomerRequestsStorage
        fields = "__all__"
