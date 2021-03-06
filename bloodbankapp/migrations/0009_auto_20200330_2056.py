# Generated by Django 3.0.4 on 2020-03-30 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbankapp', '0008_auto_20200330_1900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_male',
        ),
        migrations.AddField(
            model_name='hospital',
            name='working_days',
            field=models.CharField(default='Monday-Sunday', max_length=100),
        ),
        migrations.AddField(
            model_name='hospital',
            name='working_hours',
            field=models.CharField(default='8:00AM-5:00PM', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Male'), (1, 'Female')], default=0),
        ),
    ]
