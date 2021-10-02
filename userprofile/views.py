
from userprofile.signup import SignUpForm
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
# Create your views here.

class SignUpView(generic.CreateView):
    template_name='registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

def LoginView(request):
    pass