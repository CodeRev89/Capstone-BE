from datetime import datetime
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser,User


# Create your models here.
# class User(AbstractUser):
#     is_trainer = models.BooleanField(default=False)

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
    reps =models.IntegerField(blank=False, default=5)  
    sets =models.IntegerField(blank=False,default=5)  
    time =models.TimeField(default="10:00") 
    done =  models.BooleanField(default=False)

    def __str__(self):
        return self.exercise.name

class Subscription(models.Model):
    
    name =models.CharField(max_length=250) 
    price =models.IntegerField(blank=False) 
    describtion =models.CharField(max_length=250)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True,related_name="subs")  
    duration = models.IntegerField(blank=False) 

    def __str__(self):
        return self.name 

class SubscriptionItem(models.Model):
    plan = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True,related_name="items")  
    trainee = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True,related_name="trainees")  
    start_date = models.DateField(auto_now=True) 
    end_date = models.DateField()
    active = models.BooleanField()
    payment_status = models.BooleanField()
    auto_renew = models.BooleanField()

    def __str__(self):
        return f'{self.trainee.user.username} - {self.plan.name} '



# Chat Models 