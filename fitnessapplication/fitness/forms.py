from django import forms
from .models import Exercise, ExerciseItem, Subscription, Trainer,User



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
        fields = ["name", "short_description", "category", "image", "video"]

        def __init__(self, *args, **kwargs):
            super(ExerciseForm, self)
            self.fields['name'].widget.attrs.update({'class': 'input-group', 'label': self.kwargs["name"]})
            self.fields['short_description'].widget.attrs.update({'class': 'input-group'})
            self.fields['category'].widget.attrs.update({'class': 'input-group'})
            self.fields['image'].widget.attrs.update({'class': 'input-group'})
            self.fields['video'].widget.attrs.update({'class': 'input-group'})


class ExerciseItemForm(forms.ModelForm):
    class Meta:
        model = ExerciseItem
        fields = ["exercise", "reps", "sets", "time", "date"]
 
   
class TrainerSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["name", "price", "description",  "duration"]
        

class EditTrainerProfileForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ["age", "experience", "specialty", "image", "bio"]