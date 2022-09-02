# Generated by Django 4.0.5 on 2022-09-01 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0002_exerciseitem_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='image',
            field=models.ImageField(default='', upload_to='exercises/'),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='age',
            field=models.IntegerField(blank=True, default=25, null=True),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='height',
            field=models.IntegerField(default=165, null=True),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='image',
            field=models.ImageField(default='https://t4.ftcdn.net/jpg/00/64/67/63/240_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg', upload_to='trainees/'),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='weight',
            field=models.IntegerField(default=70, null=True),
        ),
    ]
