from django.contrib import admin

from .models import Category, Subscription, SubscriptionItem, Trainee, Trainer,Exercise,ExerciseItem,User

# Register your models here.

admin.site.register(User)
admin.site.register(Trainer)
admin.site.register(Trainee)
admin.site.register(Category)
admin.site.register(Exercise)
admin.site.register(ExerciseItem)
admin.site.register(Subscription)
admin.site.register(SubscriptionItem)
