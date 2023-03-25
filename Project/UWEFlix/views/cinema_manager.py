import requests
from django.shortcuts import redirect, render

from ..models import Club, Film, Showing, Ticket

# Create your views here.
def cm_dash(request):
    
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')
    
    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')


    return render(request, 'cm/dash.html')