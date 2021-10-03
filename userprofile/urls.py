from userprofile import views
from django.urls import path,include
from . import views

urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('redirect/',views.NewLogin,name='my_account'),
    path('users/<str:username>/',views.MainPage,name='main_page')
]