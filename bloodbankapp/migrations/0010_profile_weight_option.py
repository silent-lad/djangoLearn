# Generated by Django 3.0.4 on 2020-04-07 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbankapp', '0009_auto_20200330_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='weight_option',
            field=models.IntegerField(choices=[(0, 'Above 50'), (1, 'Below 50')], default=1),
        ),
    ]
