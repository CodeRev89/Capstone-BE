from django import forms
from .models import Trainer, TrainerWorkout





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
    
    
    
class TrainerWorkoutForm(forms.ModelForm):
    class Meta:
        model = TrainerWorkout
        fields = ["title", "short_description", "workout_type", "image"]