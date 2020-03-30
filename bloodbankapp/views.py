from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django import forms
from django.http import HttpResponse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Hospital, Appointment
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.age = form.cleaned_data.get('age')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.bloodGroup = form.cleaned_data.get('bloodGroup')
            user.profile.weight = form.cleaned_data.get('weight')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('loginUser')
    else:
        form = UserRegisterForm()
    return render(request, 'bloodbankapp/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'bloodbankapp/profile.html', context)


class HospitalListView(ListView):
    model = Hospital
    template_name = 'bloodbankapp/hospitals.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'hospitals'


class HospitalDetailView(DetailView):
    model = Hospital


class HospitalCreateView(LoginRequiredMixin, CreateView):
    model = Hospital
    fields = ['name', 'city', 'map_url']

    def form_valid(self, form):
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     # if self.request.user.username == 'blooddonation.app0@gmail.com':
    #     return True
        # return False


class HospitalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hospital
    email = forms.EmailField()
    fields = ['city', 'name', 'map_url']

    def form_valid(self, form):
        # form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # hospital = self.get_object()
        return True
        if self.request.user.email == 'blooddonation.app0@gmail.com':
            return True
        return False


class HospitalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hospital
    success_url = '/hospitals'

    def test_func(self):
        post = self.get_object()
        return True
        # if self.request.user.username == 'blooddonation.app0@gmail.com':
        # return True
        # return False


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'bloodbankapp/appointments.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'appointments'


class AppointmentForm(forms.ModelForm):
    time = forms.TimeField(
        label='Time',
        widget=forms.widgets.TimeInput(attrs={'type': 'time'}),
    )
    date = forms.DateField(
        label='Date',
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Appointment
        fields = ['time', 'date']


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        hospitalid = self.kwargs['hospitalid']
        form.instance.hospital = Hospital.objects.filter(id=hospitalid).first()
        return super().form_valid(form)

    def test_func(self):
        # post = self.get_object()
        # if self.request.user.username == 'blooddonation.app0@gmail.com':
        # return True
        return False


class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    success_url = '/appointments'

    def test_func(self):
        post = self.get_object()
        return True
        # if self.request.user.username == 'blooddonation.app0@gmail.com':
        # return True
        # return False


def index(request):
    return render(request, 'bloodbankapp/index.html')


def loginAdmin(request):
    return render(request, 'bloodbankapp/login.html', {'userType': 'admin'})


def loginUser(request):
    return render(request, 'bloodbankapp/login.html', {'userType': 'user'})


# def test(request):
#     context = {
#         'hospitals': hospitals,
#         'title': 'Hospitals'
#     }
#     return render(request, 'bloodbankapp/dashboard.html', context)
