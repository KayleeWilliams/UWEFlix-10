from django.shortcuts import redirect, render
from ..forms import PaymentForm
from ..models import Booking, Club, Accounting, Request

# CLUB REP Account to view monthly statements

def account(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user).prefetch_related('ticket_type_quantities')
        clubs = Club.objects.filter(representative=request.user)
        account = Accounting.objects.get(user=request.user)

        for booking in bookings:
            total_quantity = 0
            for ttq in booking.ticket_type_quantities.all():
                total_quantity += ttq.quantity
            booking.total_quantity = total_quantity

        # Get requests
        rep_request = False
        if Request.objects.filter(request_value=True, request_type="club").exists():
            rep_request = True
            
        return render(request, 'account.html', {'bookings': bookings, 'clubs': clubs, 'account': account, 'rep_request': rep_request})
    else:
        # Redirect to login page
        return redirect('/login')
    
def payment(request):
    if request.user.is_authenticated:
        account = Accounting.objects.get(user=request.user)
        # Check if balance is negative
        initial_amount = 10.00
        if account.balance < 0:
            initial_amount = -account.balance

        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data.get('amount')
                account.balance += amount
                account.save()
                return redirect('/account')
            else:
                form = PaymentForm(initial={'amount': initial_amount})
                return render(request, 'payment.html', {'form': form, 'account': account})
            
        form = PaymentForm(initial={'amount': initial_amount})
        return render(request, 'payment.html', {'form': form, 'account': account})
    else:
        # Redirect to login page
        return redirect('/login')
    