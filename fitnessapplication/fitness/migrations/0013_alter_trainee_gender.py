# Generated by Django 4.0.5 on 2022-09-05 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0012_alter_trainee_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainee',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True),
        ),
    ]