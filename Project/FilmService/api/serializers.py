from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Film

# Serialise film
class FilmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Film
        fields = ['title', 'age_rating', 'duration', 'description', 'imdb', 'image_url', 'backdrop_url']