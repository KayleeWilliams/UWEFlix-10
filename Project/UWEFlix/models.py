from django.db import models

# Create your models here.
class Screen(models.Model):
        capacity = models.IntegerField()

class Showing(models.Model):
        film = models.ForeignObject(Film, on_delete=models.CASCADE)
        date = models.DateField()
        time = models.TimeField()
        tickets_sold = models.IntegerField()
        screen = models.ForeignKey(Screen, on_delete=models.CASCADE)