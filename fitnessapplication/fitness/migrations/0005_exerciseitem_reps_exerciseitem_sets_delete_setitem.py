# Generated by Django 4.0.5 on 2022-08-30 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0004_subscription_subscriptionitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseitem',
            name='reps',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='exerciseitem',
            name='sets',
            field=models.IntegerField(default=5),
        ),
        migrations.DeleteModel(
            name='SetItem',
        ),
    ]
