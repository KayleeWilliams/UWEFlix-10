from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Ticket, Booking


class LoginForm(forms.Form):
    # email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()

class BookingForm(forms.Form):

    # Create a field for each available ticket type
    
    def __init__(self, *args, **kwargs):
        available_tickets = kwargs.pop('available_tickets')
        super().__init__(*args, **kwargs)
        for ticket in available_tickets:
          self.fields[f'ticket_{ticket.id}'] = forms.IntegerField(
              label=ticket.name,
              initial=0,
              min_value=0,

              # Add price as data attribute to use in JavaScript
              widget=forms.NumberInput(attrs={'data-price': ticket.price})
          )