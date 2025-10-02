from django.shortcuts import render, redirect

# Create your views here.

# General
def inicio(request):
    return render(request, 'home.html')
def home(request):
    return render(request, "home.html")
def acerca(request):
    return render(request, "acerca.html")
def habitaciones(request):
    return render(request, "habitaciones.html")
def spa(request):
    return render(request, "spa.html")
def restaurante(request):
    return render(request, "restaurante.html")
def proximamente(request):
    return render(request, "proximamente.html")

