from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Product
from django import forms
from django.contrib.auth.forms import UserCreationForm


class signUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required': "",
            'placeholder': "Username",
            'class': "email",
            'name': "username",
        })
        self.fields['email'].widget.attrs.update({
            'required': "",
            'placeholder': "email",
            'class': "email",
            'name': "email",
        })
        self.fields['password1'].widget.attrs.update({
            'required': "",
            'placeholder': "password",
            'class': "email",
            'name': "password",
        })
        self.fields['password2'].widget.attrs.update({
            'required': "",
            'placeholder': " confirm-password",
            'class': "email",
            'name': "confirm-password",
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductForm (ModelForm):
    class Meta:
        model = Product
        fields ="__all__"
