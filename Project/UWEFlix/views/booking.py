import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse

from ..forms import BookingForm
from ..models import Showing, Booking, Ticket, TicketTypeQuantity

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
                return render(request, 'booking/booking.html', {'form': form, 'showing': showing})

            # If no seats selected
            if total_tickets == 0:
                form.add_error(None, 'Please select at least 1 ticket.')
                return render(request, 'booking/booking.html', {'form': form, 'showing': showing})

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
                        return render(request, 'booking/booking.html', {'form': form, 'showing': showing})

                booking = Booking.objects.create(
                    showing=showing,
                    email=email,
                    total_cost=total_cost,
                )

            else:
                booking = Booking.objects.create(
                    showing=showing,
                    user=request.user,
                    total_cost=total_cost,
                )

            # Verify Payment Details by External system
            # If payment details are invalid
            # form.add_error(None, 'Payment Unsuccessful.')
            # return render(request, 'booking.html', {'form': form, 'showing': showing})

            # Create the booking

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
    return render(request, 'booking/booking.html', {'form': form, 'showing': showing})