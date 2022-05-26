from ckeditor.widgets import CKEditorWidget
from company.models import Company
from django import forms
from event.models import (
    Event,
    EventRentalProducts,
    EventTeam,
    RentalProducts,
)
from event.services.constants import BASE_CONTRACT


class TimePickerInput(forms.TimeInput):
    input_type = "time"


class DatePickerInput(forms.TimeInput):
    input_type = "date"


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ("contract", "contract_template")

        widgets = {
            "opening": TimePickerInput(),
            "closing": TimePickerInput(),
            # "date" : DatePickerInput()
        }

    # def __init__(self, *args, **kwargs):
    #     super(EventForm, self).__init__(*args, **kwargs)

    #     self.fields["contract_template"].initial = BASE_CONTRACT


class EventEditForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ("contract", "contract_template")

        widgets = {
            "opening": TimePickerInput(),
            "closing": TimePickerInput(),
        }


class EventTeamForm(forms.ModelForm):
    class Meta:
        model = EventTeam
        fields = "__all__"


class RentalProductsForm(forms.ModelForm):
    class Meta:
        model = RentalProducts
        fields = "__all__"


class EventRentalProductsForm(forms.ModelForm):
    class Meta:
        model = EventRentalProducts
        fields = "__all__"
