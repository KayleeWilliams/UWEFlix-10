from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Ticket, Booking


class LoginForm(forms.Form):
    # email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()

class BookingForm(forms.Form):

    # contact info
    email = forms.EmailField(required=False)

    # Card info
    card_name = forms.CharField(required=False)
    card_number = forms.CharField(required=False)
    card_expiry = forms.CharField(required=False)
    card_cvv = forms.CharField(required=False)



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

# Account form for account manager
class AccountForm(forms.Form):
    title = forms.CharField(max_length=100, required= True, label="Account Title")
    card_number = forms.IntegerField(max_length=16, required=True, label="Card Number")
    expiry_date = forms.DateField(required= True, label="Expiry Date")
    discount_rate = forms.DecimalField(required=True, label="Discount Rate")