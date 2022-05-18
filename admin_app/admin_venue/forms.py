from customer.models import (Customer, CustomerAccess, CustomerContacts,
                             CustomerRequestsStorage)
from django import forms
from venue.models import (Venue, VenueAccess, VenueContacts, VenuePictures,
                          VenueRequestsStorage)


class TimePickerInput(forms.TimeInput):
        input_type = 'time'   
    
class VenueForm(forms.ModelForm):
    
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
    

class VenueAccessForm(forms.ModelForm):
    
    class Meta:
        model = VenueAccess
        fields = "__all__"
    

class VenueRequestStorageForm(forms.ModelForm):
    
    
    class Meta:
        model = VenueRequestsStorage
        fields = "__all__"


class VenuePictureForm(forms.ModelForm):
    
    class Meta:
        model = VenuePictures
        fields = "__all__"
