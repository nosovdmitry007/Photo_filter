from django.contrib.auth.forms import UserCreationForm
from django.forms import PasswordInput

from .models import ParserUser
from django import forms




class RegistrationForm(UserCreationForm):


    class Meta:
        model = ParserUser
        fields = ('username', 'password1', 'password2', 'email')

