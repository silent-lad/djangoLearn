# Generated by Django 3.0.4 on 2020-04-09 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbankapp', '0011_remove_profile_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.IntegerField(choices=[], default=1),
        ),
    ]
