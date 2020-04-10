from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Hospital, Appointment
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.IntegerField()
    gender = forms.ChoiceField(
        choices=[(1, 'Male'), (0, 'Female')])
    age = forms.IntegerField()
    weight_option = forms.ChoiceField(
        choices=[(1, 'Above 50'), (0, 'Below 50')])
    bloodGroup = forms.CharField(max_length=3)

    def clean_weight_option(self):
        weight_option = int(self.cleaned_data['weight_option'])
        print(type(weight_option))
        if weight_option != 1:
            raise ValidationError("Can't donate blood with weight under 50")
        return weight_option

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'age',
                  'email', 'phone', 'age', 'weight_option', 'gender', 'bloodGroup']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'gender', 'age', 'weight_option', 'bloodGroup']


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'gender', 'age', 'weight_option', 'bloodGroup']
