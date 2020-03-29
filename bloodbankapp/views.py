from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

hospitals = [
    {
        'name': 'Daryaganj'
    }, {
        'name': 'GTB'
    }, {
        'name': 'MCD'
    }
]


def index(request):
    return render(request, 'bloodbankapp/index.html')


def loginAdmin(request):
    return render(request, 'bloodbankapp/login.html', {'userType': 'admin'})


def loginUser(request):
    return render(request, 'bloodbankapp/login.html', {'userType': 'user'})


def test(request):
    context = {
        'hospitals': hospitals,
        'title': 'Hospitals'
    }
    return render(request, 'bloodbankapp/dashboard.html', context)
