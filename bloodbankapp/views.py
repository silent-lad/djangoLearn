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
    return HttpResponse("Hello, world. You're at the admin portal index.")


def test(request):
    context = {
        'hospitals': hospitals,
        'title': 'Hospitals'
    }
    return render(request, 'bloodbankapp/dashboard.html', context)
