from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Hospital, Appointment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.IntegerField()
    # gender = forms.RadioSelect(choices=('male', 'female'))
    age = forms.IntegerField()
    weight = forms.IntegerField()
    bloodGroup = forms.CharField(max_length=3)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'age',
                  'email', 'phone', 'age', 'weight', 'bloodGroup']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class HospitalAddForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Hospital
        fields = ['name', 'city', 'map_url']


class HospitalUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Hospital
        fields = ['name', 'city', 'map_url']


class AppointmentAddForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Appointment
        fields = ['hospital', 'user', 'start_time']


class AppointmentUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Appointment
        fields = ['hospital', 'user', 'start_time']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'is_male', 'age', 'weight', 'bloodGroup']


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'is_male', 'age', 'weight', 'bloodGroup']
