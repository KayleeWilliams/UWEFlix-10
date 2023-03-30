from django.shortcuts import redirect, render

from ..models import Showing, Film, Screen, Ticket
from .cm.film import *
from .cm.showings import *
from .cm.screens import *
from .cm.tickets import *

# Create your views here.


def cm_dash(request):

    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    return render(request, 'cm/dash.html')


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

    else:
        return redirect('/cinema_management')
