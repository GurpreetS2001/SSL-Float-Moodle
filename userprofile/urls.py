from userprofile import views
from django.urls import path,include
from . import views

urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('redirect/',views.NewLogin,name='my_account'),
    path('',views.MainPage,name='main_page'),
    path('courses/add_new_course/',views.addCourse,name='add_course'),
    path('courses/register/',views.registerCourse,name='register_course'),
    
    path('users/<str:username>/',views.profilePage,name='profile_page'),
    path('courses/<str:name>/add_new_assignment/',views.addAssign,name='add_assign'),
    path('courses/<str:name>/assignment/<int:id>/',views.viewAssign,name='view_assign'),
    ####
    path('courses/<str:name>/<str:lecture_num>/',views.coursePage,name='course_page'),
    path('changepass/',views.PasswordChangeView.as_view(),name='change_password'),
    path('updateprofile/',views.changeUserProfile,name='updateProfile'),
    path('courses/<str:name>/assignment/<int:id>/upload_csv',views.CsvFeedbackView,name='upload_csv'),
    path('courses/<str:name>/course_stats/',views.viewCourseStats,name='course_stats')
]