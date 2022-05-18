
from artist.models import Artist, ArtistAssets
from django import forms


class ArtistAddForm(forms.ModelForm):
    
    
    class Meta:
        model = Artist
        fields = "__all__"

    
class ArtistAssetsForm(forms.ModelForm):
    
    
    class Meta:
        model = ArtistAssets
        fields = "__all__"
