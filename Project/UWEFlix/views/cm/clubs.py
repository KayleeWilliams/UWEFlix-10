from django.shortcuts import render
from django.contrib.auth.models import User

from ...forms import ClubForm
from ...models import Club

def add_club(request):

    if request.method == 'POST':
        # Get form inputs
        form = ClubForm(request.POST)

        if form.is_valid():
            # Get form inputs
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            rep = form.cleaned_data['representative']
            
            # Check not null
            for data in [name, address, phone_number, email, rep]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/clubs/form.html', {'form': form, 'action': 'Add'})


            # Get user from rep
            club_rep = User.objects.get(id=rep)

            # Create club
            club = Club.objects.create(
                name=name, address=address, phone_number=phone_number, email=email, representative=club_rep)
            club.save()


            return render(request, 'cm/success.html', {'message': 'Club added successfully', 'redirect': 'clubs_management', 'redirect_text': 'Club Management'})

    # Get all users that are club reps and not in a club
    users = User.objects.all() 

    form = ClubForm()
    return render(request, 'cm/clubs/form.html', {'form': form, 'action': 'Add', 'users': users})


def modify_club(request):
    
    # Get club
    club = Club.objects.get(id=request.GET.get('club'))

    if request.method == 'POST':
        # Get form inputs
        form = ClubForm(request.POST)

        if form.is_valid():
            # Get form inputs
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            rep = form.cleaned_data['representative']

            # Check not null
            for data in [name, address, phone_number, email, rep]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/clubs/form.html', {'form': form, 'action': 'Edit'})

            # Get user from rep
            club_rep = User.objects.get(id=rep)

            # Create club
            club.name = name
            club.address = address
            club.phone_number = phone_number
            club.email = email
            club.representative = club_rep
            club.save()

            return render(request, 'cm/success.html', {'message': 'Screen modified successfully', 'redirect': 'screens_management', 'redirect_text': 'Screen Management'})

    # Get all users that are club reps and not in a club
    users = User.objects.all()

    form = ClubForm()
    return render(request, 'cm/clubs/form.html', {'form': form, 'action': 'Edit', 'users': users})

def delete_club(request):
    club = Club.objects.get(id=request.GET.get('club'))
    club.delete()

    return render(request, 'cm/success.html', {'message': 'Club deleted successfully', 'redirect': 'clubs_management', 'redirect_text': 'Club Management'})