from django.shortcuts import redirect, render

from ...forms import ShowingForm
from ...models import Film, Screen, Showing

# Create your views here.


def showings_dash(request):

    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Get all showings
    showings = Showing.objects.all()

    return render(request, 'cm/showings/dash.html', {'showings': showings})


def add_showing(request):
    # Get films + screens
    films = Film.objects.all().order_by('title')
    screens = Screen.objects.all().order_by('capacity')

    if request.method == 'POST':
        # Get form inputs
        form = ShowingForm(request.POST)

        if form.is_valid():
            # Get form inputs
            film_id = form.cleaned_data['film_id']
            screen_id = form.cleaned_data['screen_id']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']

            # Check not null
            for data in [film_id, screen_id, date, time]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/showings/form.html', {'form': form, 'films': films, 'screens': screens, 'action': 'Create'})

            # Get the capacity of the screen and film
            screen = Screen.objects.get(id=screen_id)
            film = Film.objects.get(id=film_id)

            # Create showing
            showing = Showing.objects.create(
                film=film, screen=screen, date=date, time=time, seats=screen.capacity)
            showing.save()

            return render(request, 'cm/success.html', {'message': 'Showing added successfully', 'redirect': 'showings_management', 'redirect_text': 'Showings Management'})

    form = ShowingForm()
    return render(request, 'cm/showings/form.html', {'form': form, 'films': films, 'screens': screens, 'action': 'Create'})


def modify_showing(request):

    # Get films + screens + showing
    films = Film.objects.all().order_by('title')
    screens = Screen.objects.all().order_by('capacity')
    showing = Showing.objects.get(id=request.GET.get('showing'))

    if request.method == 'POST':
        # Get form inputs
        form = ShowingForm(request.POST)

        if form.is_valid():
            # Get form inputs
            film_id = form.cleaned_data['film_id']
            screen_id = form.cleaned_data['screen_id']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']

            # Check not null
            for data in [film_id, screen_id, date, time]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/showings/form.html', {'form': form, 'films': films, 'screens': screens, 'action': 'Modify'})

            # Get the capacity of the screen and film
            screen = Screen.objects.get(id=screen_id)
            film = Film.objects.get(id=film_id)

            # If the screen has changed then set new seats
            if showing.screen != screen:
                # Calculate total seats booked
                showing.seats = (screen.capacity - showing.seats)

            # Update showing
            showing.film = film
            showing.screen = screen
            showing.date = date
            showing.time = time

            showing.save()

            return render(request, 'cm/success.html', {'message': 'Showing added successfully', 'redirect': 'showings_management', 'redirect_text': 'Showings Management'})

    form = ShowingForm(initial={'film_id': showing.film.id,
                       'screen_id': showing.screen.id, 'date': showing.date, 'time': showing.time})
    return render(request, 'cm/showings/form.html', {'form': form, 'films': films, 'screens': screens, 'action': 'Modify'})


def delete_showing(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    if 'showing' not in request.GET:
        return redirect('/showings_management')

    # Get showing
    showing = Showing.objects.get(id=request.GET.get('showing'))

    # Delete
    showing.delete()

    # Redirect to film dash
    return render(request, 'cm/success.html', {'message': 'Showing deleted successfully', 'redirect': 'showings_management', 'redirect_text': 'Showings Management'})
