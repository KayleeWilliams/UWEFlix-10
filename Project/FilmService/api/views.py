import requests
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Film
from .serializers import FilmSerializer
from .tasks import *

# Endpoint to get all films


# Get all films
@api_view(['GET'])
def fetch_films(request):
    films = Film.objects.all()
    serializer = FilmSerializer(films, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_film(request, id):

    try:
        query = Film.objects.get(id=id)
        serializer_class = FilmSerializer

        # Update film
        response = requests.get(
            f'https://api.themoviedb.org/3/find/{query.imdb}?api_key=d4c4c2d25e196ead918fc7080850a0d7&language=en-US&external_source=imdb_id')
        data = response.json()

        # If poster or backdrop has changed since last time, update it
        for category in data.keys():
            if len(data[category]) > 0:

                if query.image_url != f"https://image.tmdb.org/t/p/original{data[category][0]['poster_path']}":
                    query.image_url = f"https://image.tmdb.org/t/p/original{data[category][0]['poster_path']}"
                    query.save()

                if query.backdrop_url != f"https://image.tmdb.org/t/p/original{data[category][0]['backdrop_path']}":
                    query.backdrop_url = f"https://image.tmdb.org/t/p/original{data[category][0]['backdrop_path']}"
                    query.save()

        return Response(status=status.HTTP_200_OK)
    except Film.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
