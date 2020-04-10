from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from .models import Hospital, Appointment, Profile, User
from datetime import datetime
from bloodbankapp.timeConversion import convertTo24Hr, convertTo12Hr


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
            user.profile.weight_option = form.cleaned_data.get('weight_option')
            user.profile.gender = form.cleaned_data.get('gender')
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


class LoginAdminForm(forms.ModelForm):
    username = forms.TextInput()
    password = forms.HiddenInput()

    class Meta:
        model = User
        fields = ['username', 'password']


class LoginAdminView(FormView):
    context_object_name = 'login_admin'
    template_name = 'bloodbank/login_admin.html'
    model = User
    form_class = LoginAdminForm

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if username == 'blooddonation.app0@gmail.com':
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/hospitals')
                else:
                    return HttpResponse("Inactive user.")
            else:
                return HttpResponseRedirect('/loginAdmin')
        else:
            return HttpResponseRedirect('/loginAdmin')


def informationView(request):
    return render(request, "bloodbankapp/information.html")


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    gender = forms.ChoiceField(
        choices=[(1, 'Male'), (0, 'Female')])
    # age = forms.IntegerField()
    weight_option = forms.ChoiceField(
        choices=[(1, 'Above 50'), (0, 'Below 50')])

    fields = ['phone', 'gender', 'weight',
              'bloodGroup', 'weight_option', 'age']

    def form_valid(self, form):
        # form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # if self.request.user.email == 'blooddonation.app0@gmail.com':
        return True
        # return False


class HospitalListView(ListView):
    model = Hospital
    template_name = 'bloodbankapp/hospitals.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'hospitals'


class HospitalDetailView(DetailView):
    model = Hospital


class HospitalCreateView(LoginRequiredMixin, CreateView):
    model = Hospital
    fields = ['name', 'city', 'map_url', 'working_days', 'working_hours']

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
    fields = ['name', 'city', 'map_url', 'working_days', 'working_hours']

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

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)


class AppointmentForm(forms.ModelForm):
    time = forms.ChoiceField()
    date = forms.DateField(
        label='Date',
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
    )

    def __init__(self, *args, **kwargs):
        hospital = kwargs.pop('hospital')
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Now you can make it dynamic.
        choices = ()
        open_time = hospital.working_hours.split('-')[0]
        close_time = hospital.working_hours.split('-')[1]

        open_time_hours = convertTo24Hr(open_time)[0]
        open_time_minutes = convertTo24Hr(open_time)[1]

        close_time_hours = convertTo24Hr(close_time)[0]
        close_time_minutes = convertTo24Hr(close_time)[1]

        temp_time_hours = open_time_hours
        temp_time_minutes = open_time_minutes
        while True:
            temp_time_minutes += 30
            if temp_time_minutes >= 60:
                temp_time_minutes -= 60
                temp_time_hours += 1
            if temp_time_hours < close_time_hours or temp_time_minutes < close_time_minutes:
                choices = choices + ((convertTo12Hr(temp_time_hours, temp_time_minutes),
                                      convertTo12Hr(temp_time_hours, temp_time_minutes)),)
            else:
                break

        self.fields.get('time').choices = choices

    class Meta:
        model = Appointment
        fields = ['time', 'date']


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm

    def get_form_kwargs(self):
        kwargs = super(AppointmentCreateView, self).get_form_kwargs()
        hospitalid = self.kwargs['hospitalid']
        kwargs.update(
            {'hospital': Hospital.objects.filter(id=hospitalid).first()})
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        hospitalid = self.kwargs['hospitalid']
        form.instance.hospital = Hospital.objects.filter(id=hospitalid).first()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hospitalid = self.kwargs['hospitalid']
        new_context_entry = Hospital.objects.filter(id=hospitalid).first()
        context["hospital"] = new_context_entry
        return context

    def test_func(self):
        # post = self.get_object()
        # if self.request.user.username == 'blooddonation.app0@gmail.com':
        # return True
        return False


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm

    def get_form_kwargs(self):
        kwargs = super(AppointmentUpdateView, self).get_form_kwargs()
        kwargs.update(
            {'hospital': self.object.hospital})
        return kwargs

    def form_valid(self, form):
        self.object = self.get_object()
        form.instance.user = self.request.user
        hospital = self.object.hospital
        form.instance.hospital = hospital
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        hospitalObject = self.object.hospital
        context["hospital"] = hospitalObject
        context["isUpdate"] = True
        return context

    def test_func(self):
        appointment = self.get_object()
        if appointment.user == self.request.user:
            return True
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
