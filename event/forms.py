from ckeditor.widgets import CKEditorWidget
from company.models import Company
from django import forms

from event.models import Event, EventArtists, RentalProducts

from .services.constants import BASE_CONTRACT


class TimePickerInput(forms.TimeInput):
        input_type = 'time'
        
class DatePickerInput(forms.TimeInput):
        input_type = 'date'

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = "__all__"
        exclude = ("contract",)
        
        widgets = {
                'opening' : TimePickerInput(),
                'closing' : TimePickerInput(),
                # "date" : DatePickerInput()
            }
    def __init__(self, company_queryset=None, venue_queryset=None, customer_queryset=None, *args, **kwargs):  
        super(EventForm, self ).__init__(*args, **kwargs)
        self.fields['company'].queryset = company_queryset
        self.fields['company'].empty_label="Please select your company"
        
        self.fields['venue'].queryset = venue_queryset
        self.fields['venue'].empty_label="Please select your venue"

        self.fields['customer'].queryset = customer_queryset
        self.fields['customer'].empty_label="Please select your customer"
        
        self.fields["contract_template"].initial = BASE_CONTRACT
        
    

class EventArtistForm(forms.ModelForm):
    
    class Meta:
        model = EventArtists
        fields = "__all__"
        exclude = ("event",)

    def __init__(self, queryset,  *args, **kwargs):   
        super(EventArtistForm, self ).__init__(*args, **kwargs)
        self.fields['artist'].empty_label="Please select artist"
        self.fields['artist'].queryset = queryset
        
        
        
class EventArtistEditForm(forms.ModelForm):
    
    class Meta:
        model = EventArtists
        fields = "__all__"
        exclude = ("event", "artist")
        

    
        
class EventProductForm(forms.Form):
    
    name = forms.CharField(max_length=100)
    picture = forms.FileField()
    price = forms.IntegerField()
    count = forms.IntegerField()
    
    
    def __init__(self, *args, **kwargs):
        super(EventProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = "Name"
        self.fields['price'].widget.attrs['placeholder'] = "Price"
        self.fields['count'].widget.attrs['placeholder'] = "Count"
        


class EventProductEditForm(forms.Form):
    
    name = forms.CharField(max_length=100)
    picture = forms.FileField()
    price = forms.IntegerField()
    count = forms.IntegerField()
    

       
class ContractForm(forms.Form):
    
    contract = forms.CharField(widget = CKEditorWidget())

    def __init__(self, *args, **kwargs):  
        super(ContractForm, self ).__init__(*args, **kwargs)
       
        
        self.fields["contract"].initial = BASE_CONTRACT