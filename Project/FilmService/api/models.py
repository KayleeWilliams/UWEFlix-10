from django.db import models

# Create your models here.

# Screen Model


class Screen(models.Model):
    capacity = models.IntegerField()

    class Meta:
        app_label = 'UWEFlix'


class Film(models.Model):
    title = models.CharField(max_length=250)
    age_rating = models.CharField(max_length=3)
    duration = models.IntegerField()
    description = models.CharField(max_length=500)
    imdb = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    backdrop_url = models.URLField(blank=True, null=True)

    class Meta:
        app_label = 'UWEFlix'


# Film Showings Model
class Showing(models.Model):
    film = models.ForeignKey(
        Film, on_delete=models.CASCADE, related_name="showings")
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField()
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)

    class Meta:
        app_label = 'UWEFlix'
