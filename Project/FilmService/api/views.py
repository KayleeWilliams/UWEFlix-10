from django.shortcuts import render
from .models import Film
# Create your views here.
from rest_framework import viewsets
from .serializers import FilmSerializer

# Endpoint to get all films
class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
