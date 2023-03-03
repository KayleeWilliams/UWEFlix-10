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


class ClubRep(models.Model):
        fist_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        date_of_birth = models.DateField()
        club = models.ForeignKey(Club, on_delete=models.CASCADE)

class Club(models.Model):
        name = models.CharField(max_length=20)
        address = models.CharField(max_length=50)
        contacts = models.IntegerField() #Landline, mobile and e-Mail
        representative = models.CharField(max_length=150) #First name, last name and date of birth.   