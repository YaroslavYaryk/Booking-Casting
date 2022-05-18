
from django import forms
from users.models import User, UserAbilities


class UserForm(forms.ModelForm):
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control" }))
    
    class Meta:
        model = User
        fields = "__all__"
        exclude = ("last_login",)
        
class UserUpdateForm(forms.ModelForm):
    
   
    class Meta:
        model = User
        fields = "__all__"
        exclude = ("last_login", "password")


class PasswordChangeForm(forms.Form):
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control" }))
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control" }))
    


    
class UserAbilitiesForm(forms.ModelForm):
    
    class Meta:
        model = UserAbilities
        fields = "__all__"

