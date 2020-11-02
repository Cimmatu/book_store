from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Product


class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(min_length=5, max_length=40)
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductForm(ModelForm):
    #name = forms.CharField(max_length=40, min_length=1)
    #rice = forms.FloatField()
    #digital = forms.BooleanField()
    #image = forms.ImageField()
    class Meta:
        model = Product
        fields = '__all__'