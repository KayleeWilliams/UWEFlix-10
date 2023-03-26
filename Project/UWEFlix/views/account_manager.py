from django.shortcuts import redirect, render

from ..forms import AccountForm, ModifyAccountForm
from ..models import Account, Club

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
            # Delete selected account
            Account.objects.filter(id=account).delete()
            return redirect('/account_management')

        return redirect('/account_management')

    # Get sorted list of accounts to view in page
    accounts = Account.objects.all().order_by('title')

    return render(request, 'am/select_account.html', {'accounts': accounts})


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
            return render(request, 'am/add_account.html', {'form': account_form, 'clubs': clubs})

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
            return render(request, 'am/add_account.html', {'form': account_form, 'clubs': clubs})

        # save new account
        new_account = Account(title=title, discount_rate=discount_rate,
                              card_number=card_number, expiry_date=expiry_date, club=club_instance)

        new_account.save()

        return redirect('/account_management')

    return render(request, 'am/add_account.html', {'form': account_form, 'clubs': clubs})


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

    return render(request, 'am/view_account.html', {'account': account_details})


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

        # if club selected
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

    return render(request, 'am/modify_account.html', {'account': account_details, 'form': account_form, 'clubs': clubs})
