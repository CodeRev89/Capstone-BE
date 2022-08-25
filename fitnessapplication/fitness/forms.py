from django import forms
from .models import Trainer





class TrainerRegister(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ["username", "first_name", "last_name", "password"]

        widgets = {
            "password": forms.PasswordInput(),
        }
        
class TrainerLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())