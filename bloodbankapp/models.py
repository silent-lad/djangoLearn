from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    is_male = models.BooleanField()
    age = models.IntegerField()
    weight = models.IntegerField()
    bloodGroup = models.CharField(max_length=3)


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    map_url = models.TextField()
    city = models.TextField()


class Appointment(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
