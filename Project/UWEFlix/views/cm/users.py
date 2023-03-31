from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.shortcuts import render

from ...forms import UserForm
from ...models import Accounting


def add_user(request):

    # Get all groups
    groups = Group.objects.all()

    if request.method == 'POST':
        # Get form inputs
        form = UserForm(request.POST)

        if form.is_valid():
            # Get form inputs
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            group_id = form.cleaned_data['group_id']
            discount = form.cleaned_data['discount']

            # Check not null
            for data in [username, password, first_name, last_name, email, group_id, discount]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/users/form.html', {'form': form, 'groups': groups, 'action': 'Add'})

            # Check username is unique
            if User.objects.filter(username=username).exists():
                form.add_error(None, 'Username already exists')
                return render(request, 'cm/users/form.html', {'form': form, 'groups': groups, 'action': 'Add'})

            # Hash password
            password = make_password(password)

            # Create user
            user = User.objects.create(
                username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            user.save()

            # Fetch group and add user to group
            group = Group.objects.get(id=group_id)
            group.user_set.add(user)
            group.save()

            # Create accounting
            accounting = Accounting.objects.create(
                user=user, discount=discount)
            accounting.save()

            return render(request, 'cm/success.html', {'message': 'User added successfully', 'redirect': 'users_management', 'redirect_text': 'User Management'})

    form = UserForm(initial={'group_id': 1})
    return render(request, 'cm/users/form.html', {'form': form, 'groups': groups, 'action': 'Add'})

# Modify User


def modify_user(request):

    # Get user
    try:
      user = User.objects.get(id=request.GET['user'])
    except: 
      return render(request, 'cm/users/dash.html')
    
    # Get accounting
    accounting = Accounting.objects.get(user=user)

    # Get all groups
    groups = Group.objects.all()

    if request.method == 'POST':
        # Get form inputs
        form = UserForm(request.POST)

        if form.is_valid():
            # Get form inputs
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            group_id = form.cleaned_data['group_id']
            discount = form.cleaned_data['discount']

            # Check not null
            for data in [username, password, first_name, last_name, email, group_id, discount]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/users/form.html', {'form': form, 'groups': groups, 'action': 'Modify'})

            # Check username is unique
            if User.objects.filter(username=username).exists():
                form.add_error(None, 'Username already exists')
                return render(request, 'cm/users/form.html', {'form': form, 'groups': groups, 'action': 'Modify'})

            # Hash password
            password = make_password(password)

            # Update User
            user.username = username
            user.password = password
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            # Fetch group and add user to group
            group = Group.objects.get(id=group_id)
            # Remove user from all groups
            for g in groups:
                g.user_set.remove(user)
            # Add user to new group
            group.user_set.add(user)
            group.save()
 
            # Update accounting
            accounting.discount = discount
            accounting.save()

            return render(request, 'cm/success.html', {'message': 'User modified successfully', 'redirect': 'users_management', 'redirect_text': 'User Management'})

    form = UserForm(initial={'username': user.username, 'password': user.password, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'group_id': user.groups.all()[0].id, 'discount': accounting.discount})
    return render(request, 'cm/users/form.html', {'form': form, 'groups': groups, 'action': 'Modify'})

# Delete User


def delete_user(request):
    # Get ticket
    user = User.objects.get(id=request.GET.get('user'))

    # Delete ticket
    user.delete()

    # Redirect to film dash
    return render(request, 'cm/success.html', {'message': 'User deleted successfully', 'redirect': 'users_management', 'redirect_text': 'User Management'})
