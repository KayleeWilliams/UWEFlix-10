from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Screen(models.Model):
        capacity = models.IntegerField()

class Showing(models.Model):
        film = models.ForeignObject(Film, on_delete=models.CASCADE)
        date = models.DateField()
        time = models.TimeField()
        tickets_sold = models.IntegerField()
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
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        total_cost = models.DecimalField(max_digits=8, decimal_places=2)

        # User can select multiple ticket types and quantities
        ticket_type_quantities = models.ManyToManyField(TicketTypeQuantity)
