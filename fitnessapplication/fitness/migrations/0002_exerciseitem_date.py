# Generated by Django 4.0.5 on 2022-09-01 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseitem',
            name='date',
            field=models.DateField(default='2022-09-01'),
        ),
    ]