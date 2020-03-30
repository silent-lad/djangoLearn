from django.urls import path, reverse

from . import views
from .views import (
    HospitalListView,
    HospitalDetailView,
    HospitalCreateView,
    HospitalUpdateView,
    HospitalDeleteView,

    AppointmentListView,
    AppointmentDeleteView,
    AppointmentCreateView
)

urlpatterns = [
    path('', views.index, name='index'),
    # path('test', views.test, name='test'),
    path('profile', views.profile, name='profile'),
    path('hospitals', HospitalListView.as_view(), name='hospital-list'),
    path('hospital/new/', HospitalCreateView.as_view(
        success_url="/hospitals"), name='hospital-create'),
    path('hospital/<int:pk>/update/',
         HospitalUpdateView.as_view(), name='hospital-update'),
    path('hospital/<int:pk>/delete/',
         HospitalDeleteView.as_view(), name='hospital-delete'),


    path('appointments', AppointmentListView.as_view(), name='appointment-list'),
    path('appointment/new/<int:hospitalid>', AppointmentCreateView.as_view(),
         name='appointment-create'),
    path('appointment/<int:pk>/delete/',
         AppointmentDeleteView.as_view(), name='appointment-delete'),
]
