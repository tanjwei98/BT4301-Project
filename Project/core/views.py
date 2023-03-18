from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext

# Create your views here.

def index(request):
    return render(request, "index.html")

def form(request):
    return render(request, "forms.html")

def card(request):
    return render(request, "cards.html")

def chart(request):
    return render(request, "charts.html")

def button(request):
    return render(request, "buttons.html")

def modal(request):
    return render(request, "modals.html")

def table(request):
    return render(request, "tables.html")

def deployment(request):
    return render(request, "deployments.html")

def overview(request):
    return render(request, "overview.html")

<<<<<<< HEAD
def accuracy(request):
    return render(request, "accuracy.html")

def service_health(request):
    return render(request, "service_health.html")
=======
def datadrift(request):
    return render(request, "datadrift.html")
    
def challengers(request):
    return render(request, "challengers.html")

def modelRegistry(request):
    return render(request, "modelRegistry.html")

def humility(request):
    return render(request, "humility.html")
>>>>>>> origin/main

def homepage(request):
    return HttpResponse("Hello, world. The dashboard is under construction. Try ../app/main/")

def handler404(request):
    response = render(request, 'index.html')
    response.status_code = 404
    return response