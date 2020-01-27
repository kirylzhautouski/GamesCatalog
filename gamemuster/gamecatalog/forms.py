from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):

    birthday = forms.DateField(input_formats=['%d-%m-%Y'])

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'birthday')
