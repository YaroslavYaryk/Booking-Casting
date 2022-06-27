from django import forms

from .models import Venue, VenueContacts
from .validators import validate_phone, validate_email


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

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        zip_code = cleaned_data.get("zip_code")
        capacity = cleaned_data.get("capacity")

        if not validate_phone(phone)[0]:
            msg = validate_phone(phone)[1]
            self.add_error("phone", msg)

        try:
            int(zip_code)
        except:
            msg = "Should be all integers"
            self.add_error("zip_code", msg)

        try:
            int(capacity)
        except:
            msg = "Should be all integers"
            self.add_error("capacity", msg)


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
