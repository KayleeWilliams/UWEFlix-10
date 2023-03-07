from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(forms.Form):
    # email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()

