from django import forms

from .models import Customer, CustomerContacts


class TimePickerInput(forms.TimeInput):
        input_type = 'time'
        
class DatePickerInput(forms.TimeInput):
        input_type = 'date'

class CustomerAddForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ("name", "address", "zip_code", "city", "active", "organization_number" )


class CustomerContactsAddForm(forms.Form):
    
    contact_user = forms.ChoiceField()
    signatory_rights = forms.BooleanField( required=False)
    active = forms.BooleanField(required=False)
    role = forms.CharField(max_length=100, required=False)

    def __init__(self, contact, users, *args, **kwargs):  
        super(CustomerContactsAddForm, self ).__init__(*args, **kwargs)
        
        self.fields["contact_user"].choices = users


        self.fields["contact_user"].initial = contact.email
        self.fields["signatory_rights"].initial = contact.signatory_rights
        self.fields["active"].initial = contact.active
        self.fields["role"].initial = contact.role

