# Generated by Django 4.0.5 on 2022-09-01 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0003_alter_exercise_image_alter_trainee_age_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainee',
            name='gender',
            field=models.CharField(choices=[('Gender', 'Gender'), ('male', 'Male'), ('female', 'Female')], default='Male', max_length=10),
        ),
    ]
