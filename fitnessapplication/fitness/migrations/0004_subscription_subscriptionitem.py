# Generated by Django 4.0.5 on 2022-08-30 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0003_setitem_delete_step'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('price', models.IntegerField()),
                ('describtion', models.CharField(max_length=250)),
                ('duration', models.IntegerField()),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='fitness.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now=True)),
                ('end_date', models.DateField()),
                ('active', models.BooleanField()),
                ('payment_status', models.BooleanField()),
                ('auto_renew', models.BooleanField()),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='fitness.subscription')),
                ('trainee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trainees', to='fitness.trainer')),
            ],
        ),
    ]