from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Film, Showing


# Serialise showing
class ShowingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Showing
        fields = ['id', 'date', 'time', 'seats', 'hidden']

# Serialise film

class FilmSerializer(serializers.HyperlinkedModelSerializer):
    showings = ShowingSerializer(many=True)

    class Meta:
        model = Film
        fields = ['title', 'age_rating', 'duration', 'description',
                  'imdb', 'image_url', 'backdrop_url', 'showings']
