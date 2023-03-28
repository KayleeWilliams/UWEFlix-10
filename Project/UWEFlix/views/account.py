from django.shortcuts import redirect, render
from ..models import Booking

# CLUB REP Account to view monthly statements


def account(request):
    if request.user.is_authenticated:
        # Print user perms
        # print(request.user.get_all_permissions(), flush=True)
        print(Booking.objects.filter(user=request.user), flush=True)
        return render(request, 'account.html')
    else:
        # Redirect to login page
        return redirect('/login')
