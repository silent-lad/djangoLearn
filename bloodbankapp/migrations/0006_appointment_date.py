# Generated by Django 3.0.4 on 2020-03-30 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbankapp', '0005_remove_appointment_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='date',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
