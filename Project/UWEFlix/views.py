import requests
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import BookingForm, LoginForm, AccountForm, ModifyAccountForm
from .models import Booking, Film, Showing, Ticket, TicketTypeQuantity, Account, Club


# Create your views here.


def temp(request):
    if request.user.is_authenticated:
        # Print user perms
        print(request.user.get_all_permissions(), flush=True)
        return render(request, 'temp.html')
    else:
        # Redirect to login page
        return redirect('/login')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        # Check if form is valid
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/temp')
            else:
                form.add_error(
                    None, "Username and password do not match an account on our system.")
                return render(request, 'login.html', {'form': form, 'errors': form.errors})

        # Form is not valid
        else:
            form.add_error(None, "An unknown error occurred")
            return render(request, 'login.html', {'form': form, 'errors': form.errors})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


# If the user is logged in, log them out and redirect them to login
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('/login')
    return redirect('/login')


# Showings
def index(request):
    # Get all films from the service
    try:
      response = requests.get('http://filmservice:8001/films')
      films = response.json()

      return render(request, 'showings.html', {'films': films})
    # If the service is down
    except:
       return render(request, 'showings.html', {'films': []})

# Booking View


def booking(request):
    # Check if query string is valid
    # if not request.user.is_authenticated:
    #   return redirect('/login')

    if 'showing' not in request.GET:
        return redirect('/')

    # Check if showing exists
    try:
        showing_id = request.GET['showing']
        showing = Showing.objects.get(id=showing_id)
    except:
        return HttpResponse('Showing does not exist')

    # If the user has submitted the form
    if request.method == 'POST':
        form = BookingForm(
            request.POST, available_tickets=Ticket.objects.all())
        # If valid form
        if form.is_valid():
            total_tickets = 0
            total_cost = 0

            # Loop through each field in the form if ticket
            for field_name, quantity in form.cleaned_data.items():
                if field_name.startswith('ticket_'):
                    total_tickets += quantity

                    # Get ticket type
                    ticket_id = field_name.split('_')[1]

                    # Get ticket price
                    total_cost += (Ticket.objects.get(id=ticket_id).price * quantity)

            # If there aren't enough seats available
            if total_tickets > showing.seats:
                form.add_error(None, 'Not enough seats available.')
                return render(request, 'booking.html', {'form': form, 'showing': showing})

            # If no seats selected
            if total_tickets == 0:
                form.add_error(None, 'Please select at least 1 ticket.')
                return render(request, 'booking.html', {'form': form, 'showing': showing})


            # If the user can't debit account perm or the user is not authenticated
            if not request.user.has_perm('contenttypes.debit_account') or not request.user.is_authenticated:
                email = form.cleaned_data['email']
                
                # Get payment details
                payment_method = form.cleaned_data['card_name']
                card_number = form.cleaned_data['card_number']
                expiry_date = form.cleaned_data['card_expiry']
                cvv = form.cleaned_data['card_cvv']

                for method in [email, payment_method, card_number, expiry_date, cvv]:
                    if method == '':
                        form.add_error(None, 'Please enter all contact and payment details.')
                        return render(request, 'booking.html', {'form': form, 'showing': showing})

                booking = Booking.objects.create(
                    showing=showing,
                    email=email,
                    total_cost=total_cost,
                )

            else:
                booking = Booking.objects.create(
                    showing=showing,
                    user=request.user,
                    total_cost=total_cost,
                )

            # Verify Payment Details by External system
            # If payment details are invalid
            # form.add_error(None, 'Payment Unsuccessful.')
            # return render(request, 'booking.html', {'form': form, 'showing': showing})

            # Create the booking

            # Create ticket type quantities for each ticket type the user booked
            for field_name, quantity in form.cleaned_data.items():
                if field_name.startswith('ticket_'):
                    ticket_id = field_name.split('_')[1]
                    ticket = Ticket.objects.get(id=ticket_id)
                    ttq = TicketTypeQuantity.objects.create(
                        ticket=ticket, quantity=quantity)
                    booking.ticket_type_quantities.add(ttq)

            # Update the number of seats available
            showing.seats -= total_tickets
            showing.save()

            # Save the booking
            booking.save()

            # Redirect to the booking confirmation page
            return render(request, 'booking-confirmation.html', {'booking': booking})
        
        if not form.is_valid():
            print(form.errors, flush=True)

    # If the user has not submitted the form
    form = BookingForm(available_tickets=Ticket.objects.all())
    return render(request, 'booking.html', {'form': form, 'showing': showing})

def account(request):
    if request.user.is_authenticated:
        # Print user perms
        # print(request.user.get_all_permissions(), flush=True)
        return render(request, 'account.html')
    else:
        # Redirect to login page
        return redirect('/login')

  
    
# ACCOUNT MANAGER - Select account to View/Edit/Delete
def account_management(request):

    # Check if the user is logged 
    if not request.user.is_authenticated:
        return redirect('/login')
    
    # Check if the user has the correct permissions
    if not request.user.has_perm('contenttypes.account_manager'):
        return redirect('/')

    if request.method == 'POST':
        # Get selected account
        if request.POST.get('select_account'):
            account = request.POST['select_account']
        else:
            print('No Account Selected')
            
        # Get account action
        if request.POST.get('account_action'):
            action = request.POST['account_action']
        else:
            print('No Action Selected')
            
        # Route the action
        if action == 'view':
            return redirect('/view_account?account=' + str(account))
        elif action == 'modify':
            return redirect('/modify_account?account=' + str(account))
        elif action == 'delete':
            #Delete selected account
            Account.objects.filter(id=account).delete()
            return redirect('/account_management')
        
        return redirect('/account_management')
      
    # Get sorted list of accounts to view in page
    accounts = Account.objects.all().order_by('title')

    return render(request, 'select_account.html', {'accounts' : accounts})


# ACCOUNT MANAGER - Add new account
def add_account(request):
    
    # Check if the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login')

    # Check if the user has the correct permissions
    if not request.user.has_perm('contenttypes.account_manager'):
        return redirect('/')

    # Get form inputs
    account_form = AccountForm(request.POST)
    # Get clubs
    clubs = Club.objects.order_by('name')

    if request.method == 'POST':
        form = AccountForm(request.POST)

        # Get club selected
        if request.POST.get('select_club'):
            club = request.POST['select_club']
        else:
            account_form.add_error(None, 'Please select a club.')
            return render(request, 'add_account.html', {'form': account_form, 'clubs': clubs})

        # Check if form is valid
        if form.is_valid():
            title = form.cleaned_data['title']
            card_number = form.cleaned_data['card_number']
            expiry_date = form.cleaned_data['expiry_date']
            discount_rate = form.cleaned_data['discount_rate']
            
        # Retrieve club instance
        club_instance = Club.objects.get(id=club)
        
        # Check if club already has account
        if Account.objects.filter(club=club_instance).exists():
            account_form.add_error(None, 'Club already has an account.')
            return render(request, 'add_account.html', {'form' : account_form, 'clubs' : clubs})

        #save new account
        new_account = Account(title=title,discount_rate=discount_rate,card_number=card_number,expiry_date=expiry_date,club=club_instance)

        
        new_account.save()

        return redirect('/account_management')

    return render(request, 'add_account.html', {'form' : account_form, 'clubs' : clubs})


# ACCOUNT MANAGER - View account
def view_account(request):
    
    # Check if the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login')
    
    # Check if the user has the correct permissions
    if not request.user.has_perm('contenttypes.account_manager'):
        return redirect('/')
    
    # Get account ID
    account = request.GET['account']
        
    # Get account record
    account_details = Account.objects.get(id=account)
        
    return render(request, 'view_account.html', {'account' : account_details})


# ACCOUNT MANAGER - Modify existing account
def modify_account(request):
    
    # Check if the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login')
    
    # Check if the user has the correct permissions
    if not request.user.has_perm('contenttypes.account_manager'):
        return redirect('/')
    
    # Get account ID
    account = request.GET['account']
        
    # Get account record
    account_details = Account.objects.get(id=account)
    
    # Get modification form
    account_form = ModifyAccountForm(request.POST)
    
    # Get clubs
    clubs = Club.objects.order_by('name')

    if request.method == 'POST':
        form = ModifyAccountForm(request.POST)

        #if club selected
        if request.POST.get('select_club'):
            club = request.POST['select_club']
        else:
            print('No Club Selected')
            club = None

        # Check if form is valid
        if form.is_valid():
            title = form.cleaned_data['title']
            card_number = form.cleaned_data['card_number']
            expiry_date = form.cleaned_data['expiry_date']
            discount_rate = form.cleaned_data['discount_rate']
            
        # Validate inputs and update account record
        if club:
            club_instance = Club.objects.get(id=club)
            account_details.club = club_instance
        if title:
            account_details.title = title
        if card_number:
            account_details.card_number = card_number
        if expiry_date:
            account_details.expiry_date = expiry_date
        if discount_rate:
            account_details.discount_rate = discount_rate
          
        # Save changes  
        account_details.save()
        
        return redirect('/account_management')
        
    return render(request, 'modify_account.html', {'account' : account_details, 'form' : account_form, 'clubs' : clubs})

