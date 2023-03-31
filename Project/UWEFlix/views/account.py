from django.shortcuts import redirect, render
from ..models import Booking,Club

# CLUB REP Account to view monthly statements


def account(request):
    if request.user.is_authenticated:
        # Print user perms
        # print(request.user.get_all_permissions(), flush=True)
        bookings = Booking.objects.filter(user=request.user)
        clubs = Club.objects.filter(user=request.user)
        return render(request, 'account.html', {'bookings':bookings, 'clubs':clubs})
    else:
        # Redirect to login page
        return redirect('/login')
