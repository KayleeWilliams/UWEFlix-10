from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from ..models import Accounting, Film, Screen, Showing, Ticket, Club, Request, Booking
from .cm.film import *
from .cm.screens import *
from .cm.showings import *
from .cm.tickets import *
from .cm.users import *
from .cm.clubs import *

# Create your views here.


def cm_dash(request):

    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')
    
    # Get all requests and prepare them for display
    urs = Request.objects.all()

    for ur in urs:
        if ur.user_id is not None:
            user = User.objects.get(id=ur.user_id)
            ur.contact = user.username
        else:
            ur.contact = ur.email

        # If booking request get the booking and total cost
        if ur.request_type == 'booking':
            booking = Booking.objects.get(id=ur.request_value)
            ur.booking = booking
        
        # If discount request get the discount value
        if ur.request_type == 'discount':
            account = Accounting.objects.get(user_id=ur.user_id)
            ur.discount = f"{float(account.discount):.2f}% -> {float(ur.request_value):.2f}%"
        # Capitalise the request type
        ur.request_type = ur.request_type.title()

        if ur.request_type == 'Club':
            ur.request_type = 'Become Club Rep'

    return render(request, 'cm/dash.html', {'requests': urs})


def film_dash(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Get sorted list of films to view in page
    films = Film.objects.all().order_by('title')

    return render(request, 'cm/film/dash.html', {'films': films})

# Showings Management Dashboard


def showings_dash(request):

    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Get all showings
    showings = Showing.objects.all()

    return render(request, 'cm/showings/dash.html', {'showings': showings})

# Screen Management Dashboard


def screens_dash(request):

    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Get all showings
    screens = Screen.objects.all()

    return render(request, 'cm/screens/dash.html', {'screens': screens})


def tickets_dash(request):

    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Get all showings
    tickets = Ticket.objects.all()

    return render(request, 'cm/tickets/dash.html', {'tickets': tickets})


def users_dash(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Get all users
    users = User.objects.all().prefetch_related('accounting')

    return render(request, 'cm/users/dash.html', {'users': users})

def clubs_dash(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Get all clubs
    clubs = Club.objects.all().select_related('account')
    
    return render(request, 'cm/clubs/dash.html', {'clubs': clubs})

# Add based on request


def add(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Check if its film, showing, screen or club in the request
    if 'film' in request.GET:
        return add_film(request)

    if 'showing' in request.GET:
        return add_showing(request)

    if 'screen' in request.GET:
        return add_screen(request)

    if 'ticket' in request.GET:
        return add_ticket(request)
    
    if 'user' in request.GET:
        return add_user(request)
    
    if 'club' in request.GET:
        return add_club(request)

    else:
        return redirect('/cinema_management')

# Modify based on request


def modify(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Check if its film, showing, screen or club in the request
    if 'film' in request.GET:
        return modify_film(request)

    if 'showing' in request.GET:
        return modify_showing(request)

    if 'screen' in request.GET:
        return modify_screen(request)

    if 'ticket' in request.GET:
        return modify_ticket(request)
    
    if 'user' in request.GET:
        return modify_user(request)
    
    if 'club' in request.GET:
        return modify_club(request)

    else:
        return redirect('/cinema_management')

# Delete based on request


def delete(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Check if its film, showing, screen or club in the request
    if 'film' in request.GET:
        return delete_film(request)

    if 'showing' in request.GET:
        return delete_showing(request)

    if 'screen' in request.GET:
        return delete_screen(request)

    if 'ticket' in request.GET:
        return delete_ticket(request)
    
    if 'user' in request.GET:
        return delete_user(request)
    
    if 'club' in request.GET:
        return delete_club(request)

    else:
        return redirect('/cinema_management')
