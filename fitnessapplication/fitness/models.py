from secrets import choice
from django.utils.text import slugify
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from numpy import maximum


# Create your models here.
class User(AbstractUser):
    is_trainer= models.BooleanField(default=False)



class Trainee(models.Model):
    gender_choices = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    
    blood_choices = [
        ("O+", "O+"),
        ("O-", "O-"),
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
    ]
    
    user= models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    gender= models.CharField(max_length=10, choices=gender_choices, null=True)
    age= models.IntegerField(blank=True, null=True,default=25)
    height= models.IntegerField(null=True,default=165)
    weight= models.IntegerField(null=True,default=70)
    blood_type= models.CharField(max_length=250, choices=blood_choices, default="O+")
    bio= models.TextField(default="")
    image= models.ImageField(upload_to="trainees/", null=True, blank=True)
  
    def __str__(self):
        return F'{self.user.id} - {self.user.username}'
    

    
class Trainer(models.Model):
    user= models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    age= models.IntegerField(blank=True, null=True)
    experience= models.IntegerField(blank=True, null=True)
    specialty= models.CharField(max_length=250)
    bio= models.TextField(default="")
    image= models.ImageField(upload_to="trainers/", null=True, blank=True)

    
    def __str__(self):
        return F'{self.user.id} - {self.user.username}'



class Category(models.Model):
    name= models.CharField(max_length=250)

    def __str__(self):
        return F'{self.id} - {self.name}'




class Exercise(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, related_name="exercises")   
    name= models.CharField(max_length=250, unique=True)
    short_description= models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="exercises")  
    image=models.ImageField(upload_to="exercises/",default="static/exercise.png")
    video = models.URLField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Exercise, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("edit-exercise", kwargs={"slug": self.slug})
    
    def get_delete_url(self):
        return reverse("delete-exercise", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.name
    def get_category(self):
        return self.category.name



class ExerciseItem(models.Model):
    trainee= models.ForeignKey(Trainee, on_delete=models.CASCADE, null=True, related_name="exercises")   
    exercise= models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True, related_name="items") 
    reps= models.IntegerField(blank=False, default=5)  
    sets= models.IntegerField(blank=False, default=5)  
    time= models.TimeField(default="10:00") 
    date= models.DateField(default="2022-09-01") 
    done=  models.BooleanField(default=False)

    def __str__(self):
        return self.exercise.name
    def get_time(self):
        return self.time.strftime("%M")



class Subscription(models.Model):
    trainer= models.OneToOneField(
        Trainer, on_delete=models.CASCADE, primary_key=True) 
    name= models.CharField(max_length=250) 
    price= models.IntegerField(default=10) 
    description= models.CharField(max_length=250)
    duration= models.IntegerField(default=30) 

    def __str__(self):
        return self.name 
    def get_trainer_name(self):
        return(f"{self.trainer.user.first_name} {self.trainer.user.last_name}")



class SubscriptionItem(models.Model):
    plan= models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, related_name="items")  
    trainee= models.ForeignKey(Trainee, on_delete=models.CASCADE, null=True, related_name="trainees")  
    start_date = models.DateField() 
    end_date= models.DateField()
    active= models.BooleanField()
    payment_status= models.BooleanField()
    auto_renew= models.BooleanField()

    def __str__(self):
        return f'{self.trainee.user.username} - {self.plan.name} '

    
    def get_trainer(self):
        return f"{self.plan.trainer.user.first_name} {self.plan.trainer.user.last_name}"
    def get_price(self):
         return self.plan.price

class Rating(models.Model):
    rating= models.FloatField(default=3.0) 
    trainer= models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, related_name="ratings")  
 



