from django import forms
# from .models import Trainer, TrainerWorkout
from django.contrib.auth.models import User

from .models import Exercise, SetItem





class TrainerRegister(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password"]

        widgets = {
            "password": forms.PasswordInput(),
        }
        
class TrainerLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    
    
    
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "short_description", "category", "image","video"]
    
class SetForm(forms.ModelForm):
    class Meta:
        model = SetItem
        fields = ["rep"]