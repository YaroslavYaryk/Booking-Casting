
from django import forms

from .models import Artist, ArtistAssets


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
