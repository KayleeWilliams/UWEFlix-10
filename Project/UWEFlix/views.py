from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from .forms import LoginForm, BookingForm
from .models import Film, Showing, Ticket, TicketTypeQuantity, Booking
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
      'seats': showing.seats,
  }

# Booking View
def booking(request):
  # Check if the user is logged in and query string is valid
  if not request.user.is_authenticated:
    return redirect('/login')
  
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
      form = BookingForm(request.POST, available_tickets=Ticket.objects.all())
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

        # If payment fails
        # ...

        # Create the booking
        booking = Booking.objects.create(
            showing=showing,
            user=request.user,
            total_cost=total_cost,
        )

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

  # If the user has not submitted the form
  form = BookingForm(available_tickets=Ticket.objects.all())
  return render(request, 'booking.html', {'form': form, 'showing': showing})
