
from artist.models import (Artist, ArtistAccess, ArtistAssets, ArtistFile,
                           ArtistRequestsStorage)
from django import forms


class ArtistAddForm(forms.ModelForm):
    
    class Meta:
        model = Artist
        fields = "__all__"

    
class ArtistAssetsForm(forms.ModelForm):
    
    class Meta:
        model = ArtistAssets
        fields = "__all__"


class ArtistAccessForm(forms.ModelForm):
    
    class Meta:
        model = ArtistAccess
        fields = "__all__"

class ArtistFileForm(forms.ModelForm):
    
    # file = forms.FileField(required=False)
    
    class Meta:
        model = ArtistFile
        fields = "__all__"


class ArtistRequestStorageForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ArtistRequestStorageForm, self).__init__(*args, **kwargs)
        print(self.fields)
        # self.fields['created_at'].disabled = True

    
    class Meta:
        model = ArtistRequestsStorage
        fields = "__all__"


