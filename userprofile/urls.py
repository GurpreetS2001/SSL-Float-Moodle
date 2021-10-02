from userprofile.views import LoginView, SignUpView
from django.urls import path,include
from . import views

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
]