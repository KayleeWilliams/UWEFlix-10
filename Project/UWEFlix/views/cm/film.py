from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests
from django.shortcuts import redirect, render

from ...forms import FilmForm
from ...models import Film, Showing, Booking, Request

# Create your views here.


def add_film(request):
    if request.method == 'POST':
        # Get form inputs
        form = FilmForm(request.POST)

        if form.is_valid():
            # Get form inputs
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            duration = form.cleaned_data['duration']
            rating = form.cleaned_data['age_rating']
            imdb = form.cleaned_data['imdb']

            # Check not null
            for data in [title, description, duration, rating, imdb]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/film/form.html', {'form': form, 'action': 'Add'})

            # Create film
            film = Film.objects.create(
                title=title, description=description, duration=duration, age_rating=rating, imdb=imdb)
            film.save()

            # Update film poster + bg
            requests.put(f'http://filmservice:8001/update/{film.id}/')

            # Redirect to film dash
            return render(request, 'cm/success.html', {'message': 'Film added successfully', 'redirect': 'film_management', 'redirect_text': 'Film Management'})

    # Create form
    form = FilmForm()
    return render(request, 'cm/film/form.html', {'form': form, 'action': 'Add'})


def modify_film(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    if 'film' not in request.GET:
        return redirect('/film_management')

    if request.method == 'POST':
        # Get form inputs
        form = FilmForm(request.POST)

        if form.is_valid():
            # Get form inputs
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            duration = form.cleaned_data['duration']
            rating = form.cleaned_data['age_rating']
            imdb = form.cleaned_data['imdb']

            # Check not null
            for data in [title, description, duration, rating, imdb]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/film/form.html', {'form': form, 'action': 'Modify'})

            # Get film
            film = Film.objects.get(id=request.GET.get('film'))

            # Update film
            film.title = title
            film.description = description
            film.duration = duration
            film.age_rating = rating
            film.imdb = imdb
            film.save()

            # Update film poster + bg
            requests.put(f'http://filmservice:8001/update/{film.id}/')

            # Redirect to film dash
            return render(request, 'cm/success.html', {'message': 'Film modified successfully', 'redirect': 'film_management', 'redirect_text': 'Film Management'})

    # Get film
    film = Film.objects.get(id=request.GET.get('film'))

    # Create form
    form = FilmForm(initial={'title': film.title, 'description': film.description,
                    'duration': film.duration, 'age_rating': film.age_rating, 'imdb': film.imdb})
    return render(request, 'cm/film/form.html', {'form': form, 'action': 'Modify'})


def delete_film(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    if 'film' not in request.GET:
        return redirect('/film_management')

    # Get film and related showings
    film = Film.objects.get(id=request.GET.get('film'))

    # If delete all showings is checked
    if request.method == 'POST':
        showings = Showing.objects.filter(film_id=request.GET.get('film'))

        # Delete showings
        for showing in showings:
            if (showing.date < datetime.now().date() or (showing.date == datetime.now().date() and (datetime.combine(datetime.min, showing.time) - timedelta(minutes=1)).time() < datetime.now(ZoneInfo('Europe/London')).time())):
                showing.delete()
            else:
                # Delete showing but refund tickets first as its in the future
                # Get bookings for this showing
                bookings = Booking.objects.filter(showing_id=showing.id)
                for booking in bookings:
                    
                    # Check if the user has an account & refund
                    if booking.user:
                        booking.user.accounting.balance += booking.total_cost
                        booking.user.accounting.save()
                    # Else refund to card (not implemented)

                    # Get requests that are pending for this booking & delete them
                    requests = Request.objects.filter(request_value=booking.id)
                    for req in requests:
                        if req.request_type == "booking":
                            req.delete()

                    # Delete booking
                    booking.delete()
                showing.delete()

        # Delete film
        film.delete()
                
        return render(request, 'cm/success.html', {'message': 'Film deleted successfully', 'redirect': 'film_management', 'redirect_text': 'Film Management'})

    else:
        try: 
            showings = Showing.objects.filter(film_id=request.GET.get('film'))

            # Check if the film has any showings
            if len(showings) > 0:
                return render(request, 'cm/failure.html', {'message': 'Film has existing showings', 'redirect': 'film_management', 'redirect_text': 'Film Management'})
        except:
            pass

        # Delete film
        film.delete()

        # Redirect to film dash
        return render(request, 'cm/success.html', {'message': 'Film deleted successfully', 'redirect': 'film_management', 'redirect_text': 'Film Management'})
