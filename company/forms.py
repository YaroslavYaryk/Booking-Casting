from django import forms
from company.models import Company
from ckeditor.widgets import CKEditorWidget
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ("creator",)


class TermsForm(forms.Form):

    terms = forms.CharField(widget=CKEditorWidget())

    def __init__(self, terms, *args, **kwargs):
        super(TermsForm, self).__init__(*args, **kwargs)
        self.fields["terms"].initial = terms


class CompanyProductsForm(forms.Form):

    product_type = forms.CharField(max_length=150)
    product_name = forms.CharField(max_length=150)
    in_stock = forms.IntegerField()
    price = forms.FloatField()
