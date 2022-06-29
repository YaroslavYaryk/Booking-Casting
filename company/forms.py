from django import forms
from company.models import Company
from ckeditor.widgets import CKEditorWidget
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        organization_number = cleaned_data.get("organization_number")
        zip_code = cleaned_data.get("zip_code")

        try:
            int(organization_number)
        except:
            msg = "Should be all integers"
            self.add_error("organization_number", msg)

        if Company.objects.filter(organization_number=organization_number):
            msg = "This organization_number already exists"
            self.add_error("organization_number", msg)

        try:
            int(zip_code)
        except:
            msg = "Should be all integers"
            self.add_error("zip_code", msg)


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


class CompanyProductsEditForm(forms.Form):

    product_type = forms.CharField(max_length=150)
    product_name = forms.CharField(max_length=150)
    in_stock = forms.IntegerField()
    price = forms.FloatField()

    def __init__(self, p_type, p_name, p_in_stock, p_price, *args, **kwargs):
        super(CompanyProductsEditForm, self).__init__(*args, **kwargs)
        self.fields["product_type"].initial = p_type
        self.fields["product_name"].initial = p_name
        self.fields["in_stock"].initial = p_in_stock
        self.fields["price"].initial = p_price
