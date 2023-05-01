from django.shortcuts import redirect, render
from ..forms import PaymentForm, DiscountForm
from ..models import Booking, Club, Accounting, Request

# CLUB REP Account to view monthly statements

def account(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user).prefetch_related('ticket_type_quantities')
        club = Club.objects.get(representative=request.user)
        account = Accounting.objects.get(user=request.user)

        for booking in bookings:
            total_quantity = 0
            for ttq in booking.ticket_type_quantities.all():
                total_quantity += ttq.quantity
            booking.total_quantity = total_quantity

        # Get requests
        requests = {
            'discount': Request.objects.filter(user=request.user, request_type="discount").exists(),
            'club': Request.objects.filter(user=request.user, request_type="club").exists()
        }

        # If Discount form is submitted
        if request.method == 'POST':
            form = DiscountForm(request.POST)
            if form.is_valid():
                request_value = form.cleaned_data['request_value']
                Request.objects.create(user=request.user, request_type='discount', request_value=request_value).save()
                return redirect('/account')
            else:
                return redirect('/account')

        form = DiscountForm(initial={'request_value': account.discount})
        return render(request, 'account.html', {'bookings': bookings, 'club': club, 'account': account, 'requests': requests, 'form': form})
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
    