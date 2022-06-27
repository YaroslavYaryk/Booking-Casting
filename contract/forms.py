from django import forms
from ckeditor.widgets import CKEditorWidget
from datetime import date as ddd
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
        # self.fields["company"].required = False
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
        fields = (
            "artist",
            "company",
            "venue",
            "price",
            "payment_methods",
            "date",
            "comment",
            "aditional_staff",
        )
        readonly_fields = ("customer",)

        widgets = {
            "payment_methods": forms.Textarea(attrs={"rows": 2, "cols": 15}),
            "comment": forms.Textarea(attrs={"rows": 5, "cols": 15}),
        }

    def __init__(self, artists, companies, venues, *args, **kwargs):
        super(ContractArtistForm, self).__init__(*args, **kwargs)
        self.fields["venue"].queryset = venues
        self.fields["venue"].empty_label = "Please select your venue"

        self.fields["company"].queryset = companies
        # self.fields["company"].required = False
        self.fields["company"].empty_label = "Select company if you need"

        self.fields["artist"].queryset = artists
        self.fields["artist"].empty_label = "Please select your artist"

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        # venue = cleaned_data.get("venue")
        # artist = cleaned_data.get("artist")

        # if venue.contract_set.filter(date=date):
        #     msg = "Venue is taken for this date"
        #     self.add_error("venue", msg)

        # if artist.contract_set.filter(date=date):
        #     msg = "Artist is taken for this date"
        #     self.add_error("artist", msg)

        if date and date < ddd.today():
            msg = "Date cannot be in the past"
            self.add_error("date", msg)


class UserContractArtistForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = "__all__"
        exclude = ("visible", "signed", "contract_pdf_url")

        widgets = {
            "payment_methods": forms.Textarea(attrs={"rows": 2, "cols": 15}),
            "comment": forms.Textarea(attrs={"rows": 5, "cols": 15}),
        }

    def __init__(self, customers, artists, companies, venues, *args, **kwargs):
        super(UserContractArtistForm, self).__init__(*args, **kwargs)

        self.fields["customer"].queryset = customers
        self.fields["customer"].empty_label = "Please select your customer"

        self.fields["venue"].queryset = venues
        self.fields["venue"].empty_label = "Please select your venue"

        self.fields["company"].queryset = companies
        # self.fields["company"].required = False
        self.fields["company"].empty_label = "Select company if you need"

        self.fields["artist"].queryset = artists
        self.fields["artist"].empty_label = "Please select your artist"

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")

        # venue = cleaned_data.get("venue")
        # artist = cleaned_data.get("artist")

        # if venue.contract_set.filter(date=date):
        #     msg = "Venue is taken for this date"
        #     self.add_error("venue", msg)

        # if artist.contract_set.filter(date=date):
        #     msg = "Artist is taken for this date"
        #     self.add_error("artist", msg)

        if date and date < ddd.today():
            msg = "Date cannot be in the past"
            self.add_error("date", msg)


class ContractArtistEditForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = (
            "customer",
            "artist",
            "contract",
            "visible",
            "signed",
            "contract_pdf_url",
        )

        widgets = {
            "payment_methods": forms.Textarea(attrs={"rows": 2, "cols": 15}),
            "comment": forms.Textarea(attrs={"rows": 5, "cols": 15}),
        }

    def __init__(self, companies, venues, *args, **kwargs):
        super(ContractArtistEditForm, self).__init__(*args, **kwargs)
        self.fields["venue"].queryset = venues
        self.fields["venue"].empty_label = "Please select your venue"

        self.fields["company"].queryset = companies
        # self.fields["company"].required = False
        self.fields["company"].empty_label = "Select company if you need"

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")

        # venue = cleaned_data.get("venue")

        # if venue.contract_set.filter(date=date):
        #     msg = "Venue is taken for this date"
        #     self.add_error("venue", msg)

        if date and date < ddd.today():
            msg = "Date cannot be in the past"
            self.add_error("date", msg)


class UserContractArtistEditForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = "__all__"
        exclude = ("customer", "artist", "visible", "signed", "contract_pdf_url")

        widgets = {
            "payment_methods": forms.Textarea(attrs={"rows": 2, "cols": 15}),
            "comment": forms.Textarea(attrs={"rows": 5, "cols": 15}),
        }

    def __init__(self, companies, venues, *args, **kwargs):
        super(UserContractArtistEditForm, self).__init__(*args, **kwargs)

        self.fields["venue"].queryset = venues
        self.fields["venue"].empty_label = "Please select your venue"

        self.fields["company"].queryset = companies
        # self.fields["company"].required = False
        self.fields["company"].empty_label = "Select company if you need"

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")

        # venue = cleaned_data.get("venue")

        # if venue.contract_set.filter(date=date):
        #     msg = "Venue is taken for this date"
        #     self.add_error("venue", msg)

        if date and date < ddd.today():
            msg = "Date cannot be in the past"
            self.add_error("date", msg)
