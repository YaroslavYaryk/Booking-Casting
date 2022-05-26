from company.models import Company
from django import forms


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ("creator",)
