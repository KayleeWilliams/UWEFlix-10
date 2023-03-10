from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from .forms import LoginForm
from .models import Club
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password


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

  #The system will handle the table of club details and film details in a similar way.
#Only the data will be different.
@csrf_exempt 
def add_club(request):
    if 'name' in request.POST and request.POST['name']:
        c1 = request.POST['name']
    if 'address' in request.POST and request.POST['address']:
        c2 = request.POST['address']
    if 'contacts' in request.POST and request.POST['contacts']:
        c3 = request.POST['contacts']
    if 'representative' in request.POST and request.POST['representative']:
        c4 = request.POST['representative']
    club = Club(name=c1, address=c2, contacts=c3, representative=c4)
    club.save()
    return HttpResponse("Success!")      
    #pass

# If the user is logged in, log them out and redirect them to login 
def logout(request):
    if request.user.is_authenticated:
      auth_logout(request)
      return redirect('/login')
    return redirect('/login')


def index(request):
    print(make_password("password"), flush=True)
    return HttpResponse("Index")
