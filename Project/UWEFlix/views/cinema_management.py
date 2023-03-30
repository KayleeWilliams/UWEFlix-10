from django.shortcuts import redirect, render

from .cm.film import *
from .cm.showings import *

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


def showings_dash(request):

    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Get all showings
    showings = Showing.objects.all()

    return render(request, 'cm/showings/dash.html', {'showings': showings})


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

    else:
        return redirect('/cinema_management')
