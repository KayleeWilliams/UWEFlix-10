from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(forms.Form):
    # email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()

class FilmForm(forms.Form):
    title = forms.CharField()
    rating = forms.CharField()
    duration = forms.CharField()
    trailer_desc = forms.CharField()

class ClubForm(forms.Form):
    name = forms.CharField()
    address = forms.CharField()
    contacts = forms.CharField()
    representative = forms.CharField()

class ScreenForm(forms.Form):
    capacity = forms.CharField()
    seat_number = forms.CharField()

class ShowingForm(forms.Form):
    title = forms.CharField()
    date = forms.CharField()
    time = forms.CharField()

