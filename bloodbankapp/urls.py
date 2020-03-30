from django.urls import path

from . import views
from .views import (
    HospitalListView,
    HospitalDetailView,
    HospitalCreateView,
    HospitalUpdateView,
    HospitalDeleteView
)

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('', HospitalListView.as_view(), name='blog-home'),
    path('hospital/<int:pk>/', HospitalDetailView.as_view(), name='hospital-detail'),
    path('hospital/new/', HospitalCreateView.as_view(), name='hospital-create'),
    path('hospital/<int:pk>/update/',
         HospitalUpdateView.as_view(), name='hospital-update'),
    path('hospital/<int:pk>/delete/',
         HospitalDeleteView.as_view(), name='hospital-delete'),
]
