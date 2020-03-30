from django.urls import path, reverse
from django.contrib.auth.decorators import login_required
from . import views
from .views import (
    HospitalListView,
    HospitalDetailView,
    HospitalCreateView,
    HospitalUpdateView,
    HospitalDeleteView,

    AppointmentListView,
    AppointmentDeleteView,
    AppointmentCreateView,
    AppointmentUpdateView,

    ProfileUpdateView
)

urlpatterns = [
    path('', views.index, name='index'),
    # path('test', views.test, name='test'),
    path('profile', views.profile, name='profile'),
    path('profile/update/<int:pk>', login_required(ProfileUpdateView.as_view()),
         name='profile-update'),

    # Hospital Views
    path('hospitals', login_required(
        HospitalListView.as_view()), name='hospital-list'),

    path('hospital/new/', login_required(HospitalCreateView.as_view(
        success_url="/hospitals")), name='hospital-create'),

    path('hospital/<int:pk>/update/',
         login_required(HospitalUpdateView.as_view()), name='hospital-update'),

    path('hospital/<int:pk>/delete/',
         login_required(HospitalDeleteView.as_view()), name='hospital-delete'),


    # Appointment Views
    path('appointments', login_required(
        AppointmentListView.as_view()), name='appointment-list'),

    path('appointment/update/<int:pk>', login_required(
        AppointmentUpdateView.as_view()), name='appointment-edit'),

    path('appointment/new/<int:hospitalid>', login_required(AppointmentCreateView.as_view()),
         name='appointment-create'),

    path('appointment/<int:pk>/delete/',
         login_required(AppointmentDeleteView.as_view()), name='appointment-delete'),
]
