from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class SignUpForm(UserCreationForm):

    birthday = forms.DateField(input_formats=['%d-%m-%Y'],
                               widget=forms.fields.TextInput(
                attrs={'placeholder': 'Enter birthday here...'}
            ))

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Enter password here...'}
        )
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm password...'}
        )
    )

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'birthday', 'password1', 'password2')

        widgets = {
            'username': forms.fields.TextInput(
                attrs={'placeholder': 'Enter username here...'}
            ),
            'email': forms.fields.EmailInput(
                attrs={'placeholder': 'Enter email here...'}
            ),
            'first_name': forms.fields.TextInput(
                attrs={'placeholder': 'Enter first name here...'}
            ),
            'last_name': forms.fields.TextInput(
                attrs={'placeholder': 'Enter last name here...'}
            ),
        }


class AuthFormWithPlaceholders(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter username here...'}
                               )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs=
                                   {'placeholder': 'Enter password here...'}
                                   )
    )
