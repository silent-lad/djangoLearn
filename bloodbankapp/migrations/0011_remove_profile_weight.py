# Generated by Django 3.0.4 on 2020-04-08 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbankapp', '0010_profile_weight_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='weight',
        ),
    ]
