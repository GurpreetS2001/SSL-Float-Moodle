
from django.http import response
from django.urls.base import reverse
from userprofile.signup import SignUpForm
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
# Create your views here.

class SignUpView(generic.CreateView):
    template_name='registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

def NewLogin(request):
    return redirect(reverse('main_page',kwargs={'username':request.user.username}))


def MainPage(request,username):
    return response.HttpResponse('Welcome')