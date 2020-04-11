from django.shortcuts import render
from .models import Movie

from django.http import HttpResponse 

def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})