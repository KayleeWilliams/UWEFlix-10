from django.shortcuts import redirect, render

from ..models import Booking, Request

def request(request):
    # Handle booking cancel requests
    if 'booking' in request.GET:
        booking_id = request.GET['booking']
        booking = Booking.objects.get(id=booking_id)

        if booking.user is not None and booking.user == request.user:
            Request.objects.create(user=booking.user, request_type='booking', request_value=booking_id).save()
            return redirect('/cancel_booking')
        
        elif 'email' in request.GET:
            email = request.GET['email']
            if booking.email == email:
                Request.objects.create(email=email, request_type='booking', request_value=booking_id).save()
                return redirect('/')

    return redirect('/')

def reject(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    if not 'request' in request.GET:
        return redirect('/cinema_management')
    
    # Get the request id from the url & delete it
    request_id = request.GET['request']
    try:
        request = Request.objects.get(id=request_id)
        request.delete()
    except:
        # If the request doesn't exist
        return redirect('/cinema_management')
    return redirect('/cinema_management')


def accept(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')
    
    if not 'request' in request.GET:
        return redirect('/cinema_management')

    # Check if request id is in the url
    request_id = request.GET['request']
    request = Request.objects.get(id=request_id)

    # If the request is a booking request
    if request.request_type == 'booking':
        try:
            booking = Booking.objects.get(id=request.request_value)
        except: # If booking doesn't exist
            return redirect('/cinema_management')
        
        # Update the showing seats available
        total_tickets = 0
        for ttq in booking.ticket_type_quantities.all():
            total_tickets += ttq.quantity
        
        booking.showing.seats += total_tickets
        booking.showing.save()

        # Give the user a refund if logged in
        if booking.user is not None:
            booking.user.accounting.balance += booking.total_cost
            booking.user.accounting.save()

        # Else: Give the user a refund if not logged in 

        booking.delete()
        request.delete()
    
    
    return redirect('/cinema_management')

    