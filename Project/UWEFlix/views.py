from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from .forms import LoginForm

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
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Dummy error to test error handling
            user = authenticate(request, username=username, password=password)
            if user is not None:
              auth_login(request, user)
              return redirect('/temp')
            else: 
               form.add_error(None, "Username and password do not match an account on our system.")
               return render(request, 'login.html', {'form': form, 'errors': form.errors})
        else:
            form.add_error(None, "An unknown error occurred")
            return render(request, 'login.html', {'form': form, 'errors': form.errors})
    else:
      form = LoginForm()
      return render(request, 'login.html', {'form': form})
    

def logout(request):
    if request.user.is_authenticated:
      auth_logout(request)
      return redirect('/login')
    return redirect('/login')


def index(request):
    print(make_password("password"), flush=True)
    return HttpResponse("Index")
