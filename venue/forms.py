from django import forms

from .models import Venue, VenueContacts


class TimePickerInput(forms.TimeInput):
        input_type = 'time'

class VenueAddForm(forms.ModelForm):
   
    class Meta:
        model = Venue
        fields = "__all__"
        
        widgets = {
                'opening' : TimePickerInput(),
                'closing' : TimePickerInput(),
            }


class VenueContactsAddForm(forms.ModelForm):
    
    class Meta:
        model = VenueContacts
        fields="__all__"
        exclude = ("venue",)
