from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Film(models.Model):
    title = models.CharField(max_length = 250)
    age_rating = models.CharField(max_length = 3)
    duration = models.IntegerField() # 'max_length' is ignored when used with IntegerField
    description = models.CharField(max_length = 500)
    imdb = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    backdrop_url = models.URLField(blank=True, null=True)

#Screen Model
class Screen(models.Model):
        capacity = models.IntegerField()

#Film Showings Model
class Showing(models.Model):
        film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="showings")
        date = models.DateField()
        time = models.TimeField()
        seats = models.IntegerField()
        screen = models.ForeignKey(Screen, on_delete=models.CASCADE)

# Available tickets
class Ticket(models.Model):
        name = models.CharField(max_length=100)
        price = models.DecimalField(max_digits=6, decimal_places=2)

# Ticket type & quantity
class TicketTypeQuantity(models.Model):
        ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField()

# Booking Model
class Booking(models.Model):
        showing = models.ForeignKey(Showing, on_delete=models.CASCADE)
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
        email = models.EmailField(null=True)  # For unregistered customers
        total_cost = models.DecimalField(max_digits=8, decimal_places=2)

        # User can select multiple ticket types and quantities
        ticket_type_quantities = models.ManyToManyField(TicketTypeQuantity)

#Club Model
class Club(models.Model):
        name = models.CharField(max_length=20)
        address = models.CharField(max_length=50)
        contacts = models.IntegerField() #Landline, mobile and e-Mail
        representative = models.CharField(max_length=150) #First name, last name and date of birth.   

#Club Representative Model
class ClubRep(models.Model):
        fist_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        date_of_birth = models.DateField()
        club = models.ForeignKey(Club, on_delete=models.CASCADE)

#Account Model - For Account Manager
class Account(models.Model):
    title = models.CharField(max_length=100)
    discount_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=10)
    club = models.OneToOneField(Club, on_delete=models.CASCADE)