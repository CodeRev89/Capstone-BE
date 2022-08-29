from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trainee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    age=models.IntegerField(blank=True, null=True)
    height=models.IntegerField(null=True)
    weight=models.IntegerField(null=True)
    blood_type= models.CharField(max_length=250, null=True)
    

    
    def __str__(self):
        return self.user.username
    

    
class Trainer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True) # primary_key = true replaces the field id
    age=models.IntegerField(blank=True, null=True)
    experience=models.IntegerField(blank=True, null=True)
    specialty= models.CharField(max_length=250)
    
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name= models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True,related_name="exercises")   
    name= models.CharField(max_length=250)
    short_description= models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,related_name="exercises")  
    image=models.ImageField(upload_to="exercises/",default="")
    video = models.URLField(max_length=250)

    def __str__(self):
        return self.name

class ExerciseItem(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, null=True,related_name="exercises")   
    exercise= models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True,related_name="items") 

    def __str__(self):
        return self.exercise.name

class SetItem(models.Model):
    rep =models.IntegerField(blank=False)  
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True,related_name="sets")  

    def __str__(self):
        return self.reps 



# Chat Models 