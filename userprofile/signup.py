from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,required=True)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=256,required=True)

    class Meta:
        model = User
        fields = ('first_name','last_name','username','password1','password2','email')