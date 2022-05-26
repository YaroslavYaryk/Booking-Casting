from django import forms

from event.models import Event


class TimePickerInput(forms.TimeInput):
    input_type = "time"


class DatePickerInput(forms.TimeInput):
    input_type = "date"


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = (
            "contract",
            "contract_template",
        )

        widgets = {
            "opening": TimePickerInput(),
            "closing": TimePickerInput(),
            # "date" : DatePickerInput()
        }

    def __init__(self, venue_queryset=None, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["venue"].queryset = venue_queryset
        self.fields["venue"].empty_label = "Please select your venue"

        # self.fields["contract_template"].initial = BASE_CONTRACT


class EventProductForm(forms.Form):

    name = forms.CharField(max_length=100)
    picture = forms.FileField()
    price = forms.IntegerField()
    count = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(EventProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "Name"
        self.fields["price"].widget.attrs["placeholder"] = "Price"
        self.fields["count"].widget.attrs["placeholder"] = "Count"


class EventProductEditForm(forms.Form):

    name = forms.CharField(max_length=100)
    picture = forms.FileField()
    price = forms.IntegerField()
    count = forms.IntegerField()
