from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import models
from .models import Trainee, Trainer, User

@receiver(post_save, sender=User)
def created_trainee_profile(created,instance, *args, **kwargs):
    pass
    # if len(instance.groups.all()) != 0:
    #     # if instance.is_staff:
    #     #     None
    #     if "Trainers" in instance.groups.all():
    #         Trainer.objects.create(user=instance)
    #     else:
    #         Trainee.objects.create(user=instance)
