from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request,'bakery.html')

def login(request):
    return render(request,'login.html')

def reports(request):
    return render(request,'reports.html')
