from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Contract


class ContractArtistForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ("artist", "company", "venue")
        readonly_fields = ("customer",)

    def __init__(self, artists, companies, venues, *args, **kwargs):
        super(ContractArtistForm, self).__init__(*args, **kwargs)
        self.fields["venue"].queryset = venues
        self.fields["venue"].empty_label = "Please select your venue"

        self.fields["company"].queryset = companies
        self.fields["company"].required = False
        self.fields["company"].empty_label = "Select company if you need"

        self.fields["artist"].queryset = artists
        self.fields["artist"].empty_label = "Please select your artist"


class ContractForm(forms.Form):

    contract = forms.CharField(widget=CKEditorWidget())

    def __init__(self, contract, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)

        self.fields["contract"].initial = contract


class ContractArtistForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ("artist", "company", "venue")
        readonly_fields = ("customer",)

    def __init__(self, artists, companies, venues, *args, **kwargs):
        super(ContractArtistForm, self).__init__(*args, **kwargs)
        self.fields["venue"].queryset = venues
        self.fields["venue"].empty_label = "Please select your venue"

        self.fields["company"].queryset = companies
        self.fields["company"].required = False
        self.fields["company"].empty_label = "Select company if you need"

        self.fields["artist"].queryset = artists
        self.fields["artist"].empty_label = "Please select your artist"


class ContractArtistEditForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = (
            "customer",
            "contract",
        )

    def __init__(self, *args, **kwargs):
        super(ContractArtistEditForm, self).__init__(*args, **kwargs)
        # self.fields["venue"].queryset = venues
        # self.fields["venue"].empty_label = "Please select your venue"

        # self.fields["company"].queryset = companies
        self.fields["company"].required = False
        # self.fields["company"].empty_label = "Select company if you need"

        # self.fields["artist"].queryset = artists
        # self.fields["artist"].empty_label = "Please select your artist"
