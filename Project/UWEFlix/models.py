from django.db import models

# Create your models here.
class Film(models.Model):
    title = models.CharField(max_length = 250)
    ageRating = models.CharField(max_length = 3)
    duration = models.IntegerField(max_length = 3) # e.g. instead of 2 hours 20 mins, just 140 mins
    descrition = models.CharField(max_length = 500)
    imdb = models.TextField()
    image_url = models.URLfield(blank=True, null=True)
    backdrop_url = models.URLfield(blank=True, null=True)

class Screen(models.Model):
        capacity = models.IntegerField()

class Showing(models.Model):
        film = models.ForeignObject(Film, on_delete=models.CASCADE)
        date = models.DateField()
        time = models.TimeField()
        tickets_sold = models.IntegerField()
        screen = models.ForeignKey(Screen, on_delete=models.CASCADE)


class ClubRep(models.Model):
        fist_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        date_of_birth = models.DateField()
        club = models.ForeignKey(Club, on_delete=models.CASCADE)