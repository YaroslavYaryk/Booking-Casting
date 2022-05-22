
from django import forms

from .models import Artist, ArtistAssets
from ckeditor.widgets import CKEditorWidget


class ArtistAddForm(forms.ModelForm):
    
    
    class Meta:
        model = Artist
        fields = ('name', 'technical_raider', 'hospitality_raider', "active",)

class RequestForm(forms.Form):
    
    choice = forms.BooleanField(required=False)
    
    
class ArtistAssetsForm(forms.ModelForm):
    
    file = forms.FileField(required=False)
    
    class Meta:
        model = ArtistAssets
        fields = ('file', 'credit')


class TechRiderForm(forms.Form):
    
    rider = forms.CharField(widget = CKEditorWidget())

    def __init__(self, rider, *args, **kwargs):  
        super(TechRiderForm, self ).__init__(*args, **kwargs)
       
        
        self.fields["rider"].initial = rider


class HospRiderForm(forms.Form):
    
    rider = forms.CharField(widget = CKEditorWidget())

    def __init__(self, rider, *args, **kwargs):  
        super(HospRiderForm, self ).__init__(*args, **kwargs)
       
        
        self.fields["rider"].initial = rider