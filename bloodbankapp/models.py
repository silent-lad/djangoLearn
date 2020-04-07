from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True)
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    age = models.IntegerField(null=True, blank=True)
    WEIGHT_ABOVE_50 = 1
    WEIGHT_BELOW_50 = 0
    WEIGHT_CHOICES = [(WEIGHT_BELOW_50, 'Above 50'),
                      (WEIGHT_ABOVE_50, 'Below 50')]
    weight_option = models.IntegerField(choices=WEIGHT_CHOICES, default=1)
    weight = models.IntegerField(null=True, blank=True)
    bloodGroup = models.CharField(max_length=3, null=True, blank=True)

    def get_absolute_url(self):
        return f'/profile/update/{self.id}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    working_days = models.CharField(max_length=100, default='Monday-Sunday')
    working_hours = models.CharField(max_length=100, default='8:00AM-5:00PM')
    map_url = models.TextField()
    city = models.TextField()

    def get_absolute_url(self):
        return '/hospitals'


class Appointment(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(default='00:00:00', max_length=100, null=True)

    def get_absolute_url(self):
        return '/appointments'
