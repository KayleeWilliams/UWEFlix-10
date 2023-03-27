import requests
from django.shortcuts import redirect, render, HttpResponse

from ..forms import FilmForm
from ..models import Club, Film, Showing, Ticket

# Create your views here.


def cm_dash(request):

    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    return render(request, 'cm/dash.html')


def film_dash(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

    # Get sorted list of films to view in page
    films = Film.objects.all().order_by('title')

    return render(request, 'cm/film/dash.html', {'films': films})


def add_film(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
        return redirect('/')

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
    form = FilmForm(initial={'title': film.title, 'description': film.description, 'duration': film.duration, 'age_rating': film.age_rating, 'imdb': film.imdb})
    return render(request, 'cm/film/form.html', {'form': form, 'action': 'Modify'})

def delete_film(request):
    # Check if the user is logged in and cinema manager
    if not request.user.is_authenticated:
      return redirect('/login')

    if not request.user.has_perm('contenttypes.cinema_manager'):
      return redirect('/')
    
    if 'film' not in request.GET:
      return redirect('/film_management')

    # Get film
    film = Film.objects.get(id=request.GET.get('film'))

    # Delete film
    film.delete()

    # Redirect to film dash
    return render(request, 'cm/success.html', {'message': 'Film deleted successfully', 'redirect': 'film_management', 'redirect_text': 'Film Management'})