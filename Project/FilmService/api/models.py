from django.db import models

# Create your models here.


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
