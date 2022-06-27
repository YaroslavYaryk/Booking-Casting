from django import forms
from contract.models import ContractTimeClock, TimeClock, CompanyContractRentalProduct

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


class TimeClockForm(forms.ModelForm):
    class Meta:
        model = TimeClock
        fields = "__all__"

        widgets = {
            "start_time": TimePickerInput(),
            "end_time": TimePickerInput(),
            # "date" : DatePickerInput()
        }


class ArtistEventTeamForm(forms.Form):

    artist_team = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

    def __init__(self, team_users, *args, **kwargs):
        super(ArtistEventTeamForm, self).__init__(*args, **kwargs)
        self.fields["artist_team"].choices = team_users


class ConfirmEventProductForm(forms.Form):

    accept = forms.BooleanField(required=True)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     accept = cleaned_data.get("accept")

    #     if not accept:
    #         msg = "You should accept all company Terms"
    #         self.add_error("accept", msg)


class CompanyContractProduct(forms.ModelForm):
    class Meta:
        model = CompanyContractRentalProduct
        exclude = ("company", "contract", "total_price", "confirmed")

    def __init__(self, company_products, *args, **kwargs):
        super(CompanyContractProduct, self).__init__(*args, **kwargs)
        if company_products:
            self.fields["product"].queryset = company_products

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        count = cleaned_data.get("count")
        print(count, product.in_stock)
        if count > product.in_stock:
            msg = "Count is nore than products in stock"
            self.add_error("count", msg)
