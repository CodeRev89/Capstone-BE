from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Exercise, Trainee, Trainer, User
from django.utils.text import slugify

@receiver(post_save, sender=User)
def created_trainee_profile(created,instance, *args, **kwargs):
    pass
    if created:
        if instance.is_trainer:
            Trainer.objects.create(user=instance)
        else:
            Trainee.objects.create(user=instance)



@receiver(post_save, sender=Exercise)
def slugify_exercise_name(created, sender, instance, **kwargs):
    if created == True:
        instance.slug = slugify(instance.name)
        print(instance.slug)