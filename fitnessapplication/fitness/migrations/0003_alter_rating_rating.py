# Generated by Django 4.0.5 on 2022-09-07 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0002_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.FloatField(default=3.0),
        ),
    ]
