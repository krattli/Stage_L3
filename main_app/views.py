from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Bonjour depuis l'app principale".encode("utf-8"))
