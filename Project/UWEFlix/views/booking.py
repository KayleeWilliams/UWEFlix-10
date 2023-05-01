import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.shortcuts import render, redirect
from django.http import HttpResponse

from ..forms import BookingForm, EmailForm
from ..models import Showing, Booking, Ticket, TicketTypeQuantity, Accounting, User, Request

# Showings


def index(request):
    # Get all films from the service
    try:
        response = requests.get('http://filmservice:8001/films')
        films = response.json()
        return render(request, 'booking/showings.html', {'films': films})
    # If the service is down
    except:
        return render(request, 'booking/showings.html', {'films': []})

# Booking View


def booking(request):
    if 'showing' not in request.GET:
        return redirect('/')

    # Check if showing exists
    try:
        showing_id = request.GET['showing']
        showing = Showing.objects.get(id=showing_id)
    except:
        return HttpResponse('Showing does not exist')

    # Check if the showing date & time has passed
    if (showing.date < datetime.now().date() or (showing.date == datetime.now().date() and showing.time < datetime.now(ZoneInfo('Europe/London')).time())):
        return redirect("/")

    # Get the user
    user, account = None, None
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        account = Accounting.objects.get(user=user)

    # If the user has submitted the form
    if request.method == 'POST':
        form = BookingForm(
            request.POST, available_tickets=Ticket.objects.all())
        
        # Check if the form is submitted after the start time.
        if (showing.date < datetime.now().date() or (showing.date == datetime.now().date() and showing.time < datetime.now(ZoneInfo('Europe/London')).time())):
            return redirect("/")
        
        # If valid form
        if form.is_valid():
            total_tickets = 0
            total_cost = 0

            # Loop through each field in the form if ticket
            for field_name, quantity in form.cleaned_data.items():
                if field_name.startswith('ticket_'):

                    if not isinstance(quantity, int):
                        quantity = 0

                    total_tickets += quantity

                    # Get ticket type
                    ticket_id = field_name.split('_')[1]

                    # Get ticket price
                    total_cost += (Ticket.objects.get(id=ticket_id).price * quantity)

            # If there aren't enough seats available
            if total_tickets > showing.seats:
                form.add_error(None, 'Not enough seats available.')
                return render(request, 'booking/booking.html', {'form': form, 'showing': showing, 'account': account})

            # If no seats selected
            if total_tickets == 0:
                form.add_error(None, 'Please select at least 1 ticket.')
                return render(request, 'booking/booking.html', {'form': form, 'showing': showing, 'account': account})

            # If the user can't debit account perm or the user is not authenticated
            if not request.user.has_perm('contenttypes.debit_account') or not request.user.is_authenticated:
                email = form.cleaned_data['email']

                # Get payment details
                payment_method = form.cleaned_data['card_name']
                card_number = form.cleaned_data['card_number']
                expiry_date = form.cleaned_data['card_expiry']
                cvv = form.cleaned_data['card_cvv']

                for method in [email, payment_method, card_number, expiry_date, cvv]:
                    if method == '':
                        form.add_error(
                            None, 'Please enter all contact and payment details.')
                        return render(request, 'booking/booking.html', {'form': form, 'showing': showing, 'account': account})

                booking = Booking.objects.create(
                    showing=showing,
                    email=email,
                    total_cost=total_cost,
                )

            else:
                # Debit account
                account = Accounting.objects.get(user=request.user)

                # Get the discount
                total_cost = total_cost - (total_cost * (account.discount/100))
                account.balance -= total_cost
                account.save()

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
            return render(request, 'booking/booking-confirmation.html', {'booking': booking})

        if not form.is_valid():
            print(form.errors, flush=True)

    # If the user has not submitted the form
    form = BookingForm(available_tickets=Ticket.objects.all())
    return render(request, 'booking/booking.html', {'form': form, 'showing': showing, 'account': account})


def cancel_booking(request):
    if request.method == 'POST':
        # Get the email from the form
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            bookings = Booking.objects.filter(email=email)

            for booking in bookings:
                if Request.objects.filter(request_value=booking.id, request_type="booking").exists():
                    booking.requested = True

                total_tickets = 0
                for ttq in booking.ticket_type_quantities.all():
                    total_tickets += ttq.quantity
                booking.total_tickets = total_tickets

            return render(request, 'booking/cancel.html', {'bookings': bookings, 'email': email})

    # If the user is not authenticated
    if not request.user.is_authenticated:
        form = EmailForm()
        return render(request, 'booking/cancel.html', {'form': form})
    else:
        # Get the user's bookings
        bookings = Booking.objects.filter(user=request.user)

        for booking in bookings:
            if Request.objects.filter(request_value=booking.id, request_type="booking").exists():
                booking.requested = True

            total_tickets = 0
            for ttq in booking.ticket_type_quantities.all():
                total_tickets += ttq.quantity
            booking.total_tickets = total_tickets

        return render(request, 'booking/cancel.html', {'bookings': bookings})
