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

# Available tickets
class Ticket(models.Model):
        name = models.CharField(max_length=100)
        price = models.DecimalField(max_digits=6, decimal_places=2)

# Ticket type & quantity
class TicketTypeQuantity(models.Model):
        ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField()
