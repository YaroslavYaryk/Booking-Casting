from django import forms

from .models import Customer, CustomerContacts


class TimePickerInput(forms.TimeInput):
        input_type = 'time'
        
class DatePickerInput(forms.TimeInput):
        input_type = 'date'

class CustomerAddForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ("name", "address", "zip_code", "city", "active" )


class CustomerContactsAddForm(forms.ModelForm):
    
    class Meta:
        model = CustomerContacts
        exclude = ("customer",)
        
        widgets = {
                'birthdate' : DatePickerInput(),
            }
