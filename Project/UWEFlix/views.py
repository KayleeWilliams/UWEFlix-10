import requests
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import BookingForm, LoginForm
from .models import Booking, Film, Showing, Ticket, TicketTypeQuantity
from .permissions import *

# Create your views here.


def temp(request):
    if request.user.is_authenticated:
        # Print user perms
        print(request.user.get_all_permissions(), flush=True)
        return render(request, 'temp.html')
    else:
        # Redirect to login page
        return redirect('/login')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        # Check if form is valid
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/temp')
            else:
                form.add_error(
                    None, "Username and password do not match an account on our system.")
                return render(request, 'login.html', {'form': form, 'errors': form.errors})

        # Form is not valid
        else:
            form.add_error(None, "An unknown error occurred")
            return render(request, 'login.html', {'form': form, 'errors': form.errors})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


# If the user is logged in, log them out and redirect them to login
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('/login')
    return redirect('/login')


# Showings
def index(request):
    # Get all films from the service
    try:
      response = requests.get('http://filmservice:8001/films')
      films = response.json()

      return render(request, 'showings.html', {'films': films})
    # If the service is down
    except:
       return render(request, 'showings.html', {'films': []})

# Booking View


def booking(request):
    # Check if query string is valid
    # if not request.user.is_authenticated:
    #   return redirect('/login')

    if 'showing' not in request.GET:
        return redirect('/')

    # Check if showing exists
    try:
        showing_id = request.GET['showing']
        showing = Showing.objects.get(id=showing_id)
    except:
        return HttpResponse('Showing does not exist')

    # If the user has submitted the form
    if request.method == 'POST':
        form = BookingForm(
            request.POST, available_tickets=Ticket.objects.all())
        # If valid form
        if form.is_valid():
            total_tickets = 0
            total_cost = 0

            # Loop through each field in the form if ticket
            for field_name, quantity in form.cleaned_data.items():
                if field_name.startswith('ticket_'):
                    total_tickets += quantity

                    # Get ticket type
                    ticket_id = field_name.split('_')[1]

                    # Get ticket price
                    total_cost += (Ticket.objects.get(id=ticket_id).price * quantity)

            # If there aren't enough seats available
            if total_tickets > showing.seats:
                form.add_error(None, 'Not enough seats available.')
                return render(request, 'booking.html', {'form': form, 'showing': showing})

            # If no seats selected
            if total_tickets == 0:
                form.add_error(None, 'Please select at least 1 ticket.')
                return render(request, 'booking.html', {'form': form, 'showing': showing})

            # Get payment details
            payment_method = form.cleaned_data['card_name']
            card_number = form.cleaned_data['card_number']
            expiry_date = form.cleaned_data['card_expiry']
            cvv = form.cleaned_data['card_cvv']

            # Verify Payment Details by External system
            # If payment details are invalid
            # form.add_error(None, 'Payment Unsuccessful.')
            # return render(request, 'booking.html', {'form': form, 'showing': showing})

            # Create the booking
            booking = Booking.objects.create(
                showing=showing,
                user=request.user,
                total_cost=total_cost,
            )

            # Create ticket type quantities for each ticket type the user booked
            for field_name, quantity in form.cleaned_data.items():
                if field_name.startswith('ticket_'):
                    ticket_id = field_name.split('_')[1]
                    ticket = Ticket.objects.get(id=ticket_id)
                    ttq = TicketTypeQuantity.objects.create(
                        ticket=ticket, quantity=quantity)
                    booking.ticket_type_quantities.add(ttq)

            # Update the number of seats available
            showing.seats -= total_tickets
            showing.save()

            # Save the booking
            booking.save()

            # Redirect to the booking confirmation page
            return render(request, 'booking-confirmation.html', {'booking': booking})

    # If the user has not submitted the form
    form = BookingForm(available_tickets=Ticket.objects.all())
    return render(request, 'booking.html', {'form': form, 'showing': showing})

def account(request):
    if request.user.is_authenticated:
        # Print user perms
        # print(request.user.get_all_permissions(), flush=True)
        return render(request, 'account.html')
    else:
        # Redirect to login page
        return redirect('/login')
