from django.shortcuts import redirect, render
from ..forms import TopUpForm
from ..models import Booking,Club,Balance

# CLUB REP Account to view monthly statements

def account(request):
    if request.user.is_authenticated:
        # Print user perms
        # print(request.user.get_all_permissions(), flush=True)
        bookings = Booking.objects.filter(user=request.user)
        clubs = Club.objects.filter(user=request.user)
        balance = Balance.objects.filter(user=request.user)
        return render(request, 'account.html', {'bookings':bookings, 'clubs':clubs, 'balance':balance})
    else:
        # Redirect to login page
        return redirect('/login')
    
def repayment(request):
    if request.user.is_authenticated:
        return render(request, 'repayment.html')
    else:
        # Redirect to login page
        return redirect('/login')
    
def topup(request):
    if request.user.is_authenticated:
        topup_form = TopUpForm(request.POST)
        return render(request, 'topup.html', {'form':topup_form})
    else:
        # Redirect to login page
        return redirect('/login')
    
def topup(request):
    form = TopUpForm(request.POST)
    if request.POST:
        if form.is_valid():
            user = request.user
            amount = form.cleaned_data.get('amount')

            balance, created = Balance.objects.get_or_create(user=user)
            balance.balance += amount
            balance.save()
            
            return redirect('/account')

    return render(request, 'topup.html', {'form':form})
