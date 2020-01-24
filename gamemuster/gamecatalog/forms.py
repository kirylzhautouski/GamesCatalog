from django import forms

from .models import User


class SignUpForm(forms.ModelForm):

    birthday = forms.DateField(input_formats=['%d-%m-%Y'])

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=16,
                                       widget=forms.PasswordInput())

    class Meta:

        model = User

        fields = ['username', 'email', 'first_name', 'second_name', 'birthday'
                  , 'password']
