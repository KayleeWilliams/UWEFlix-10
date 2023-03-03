from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Dummy error to test error handling
            if email == password:  
              form.add_error(None, "Email and password cannot be the same.")
              return render(request, 'login.html', {'form': form, 'errors': form.errors})
            else:
              return HttpResponse("Logged In")
        else:
            form.add_error(None, "An unknown error occurred")
            return render(request, 'login.html', {'form': form, 'errors': form.errors})
    else:
      form = LoginForm()
      return render(request, 'login.html', {'form': form})


def index(request):
    return HttpResponse("Index")
