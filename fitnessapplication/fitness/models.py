from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Trainee(User):
    # age=models.IntegerField()
    # height=models.IntegerField()
    
    def __str__(self):
        return self.username
    
class Trainer(User):
    age=models.IntegerField(blank=True, null=True)
    experience=models.IntegerField(blank=True, null=True)
    specialty= models.CharField(max_length=250)
    def __str__(self):
        return self.username

    
    