from datetime import date
from django import forms

from .models import Artist, ArtistAssets, ArtistBusyDates
from ckeditor.widgets import CKEditorWidget


class ArtistAddForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = (
            "name",
            "technical_raider",
            "hospitality_raider",
            "active",
        )


class ArtistEditForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        date_created = cleaned_data.get("date_created")

        if date_created and date_created > date.today():
            msg = "Date cannot be in the future"
            self.add_error("date_created", msg)


class ArtistBusyDatesForm(forms.ModelForm):
    class Meta:
        model = ArtistBusyDates
        exclude = ("artist",)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date < date.today():
            msg = "Date cannot be in the past"
            self.add_error("start_date", msg)
        if end_date < date.today():
            msg = "Date cannot be in the past"
            self.add_error("end_date", msg)

        if end_date < start_date:
            msg = "End Date is lower than Start"
            self.add_error("end_date", msg)


class RequestForm(forms.Form):

    choice = forms.BooleanField(required=False)


class ArtistAssetsForm(forms.ModelForm):

    file = forms.FileField(required=False)

    class Meta:
        model = ArtistAssets
        fields = ("file", "credit")


class TechRiderForm(forms.Form):

    rider = forms.CharField(widget=CKEditorWidget())

    def __init__(self, rider, *args, **kwargs):
        super(TechRiderForm, self).__init__(*args, **kwargs)

        self.fields["rider"].initial = rider


class HospRiderForm(forms.Form):

    rider = forms.CharField(widget=CKEditorWidget())

    def __init__(self, rider, *args, **kwargs):
        super(HospRiderForm, self).__init__(*args, **kwargs)

        self.fields["rider"].initial = rider
