from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from .forms import LoginForm
from .models import Film
from django.contrib.auth.hashers import make_password
import requests

# Create your views here.
def temp(request):
    if request.user.is_authenticated:
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
               form.add_error(None, "Username and password do not match an account on our system.")
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
    # If the user is not logged in, redirect them to the login page
    if not request.user.is_authenticated:
      return redirect('/login')
    
    # Get all films and showings
    films = Film.objects.all().prefetch_related('showings')

    # Get film posters by IMDB ID using an API
    for film in films:
      response = requests.get(f'https://api.themoviedb.org/3/find/{film.imdb}?api_key=d4c4c2d25e196ead918fc7080850a0d7&language=en-US&external_source=imdb_id')
      data = response.json()
      for category in data.keys():
        if len(data[category]) > 0:
          # If poster or backdrop has changed since last time, update it
          if film.image_url != f"https://image.tmdb.org/t/p/original{data[category][0]['poster_path']}":
            film.image_url = f"https://image.tmdb.org/t/p/original{data[category][0]['poster_path']}"
            film.save()

          elif film.backdrop_url != f"https://image.tmdb.org/t/p/original{data[category][0]['backdrop_path']}":
            film.backdrop_url = f"https://image.tmdb.org/t/p/original{data[category][0]['backdrop_path']}"
            film.save()

    # Serialise films
    serialized_films = [film_serialisable(film) for film in films]

    return render(request, 'showings.html', {'films': serialized_films})

# Serialise Film & Showings
def film_serialisable(film):
  serialised_showings = [showing_serialisable(showing) for showing in film.showings.all()]

  return {
      'title': film.title,
      'description': film.description,
      'duration': film.duration,
      'age_rating': film.age_rating,
      'image_url': film.image_url,
      'showings': serialised_showings,
  }

def showing_serialisable(showing):
  return {
      'id': showing.id,
      'date': showing.date.strftime('%Y-%m-%d'),
      'time': showing.time.strftime('%H:%M'),
      'tickets_sold': showing.tickets_sold,
  }
