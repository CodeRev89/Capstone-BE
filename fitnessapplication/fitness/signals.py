from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import models
from .models import Trainee, User

@receiver(post_save, sender=User)
def created_trainee_profile(created,instance, *args, **kwargs):
    if created==True:
        Trainee.objects.create(user=instance)