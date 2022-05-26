from django import forms

from .models import Venue, VenueContacts


class TimePickerInput(forms.TimeInput):
    input_type = "time"


class VenueAddForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = "__all__"

        widgets = {
            "opening": TimePickerInput(),
            "closing": TimePickerInput(),
        }


class VenueContactsAddForm(forms.Form):

    venue_user = forms.ChoiceField()
    active = forms.BooleanField(required=False)
    role = forms.CharField(max_length=100, required=False)

    def __init__(self, contact, users, *args, **kwargs):
        super(VenueContactsAddForm, self).__init__(*args, **kwargs)

        self.fields["venue_user"].choices = users

        self.fields["venue_user"].initial = contact.epost
        self.fields["active"].initial = contact.active
        self.fields["role"].initial = contact.role
