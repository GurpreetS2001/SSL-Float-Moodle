from userprofile import views
from django.urls import path,include
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetCompleteView,PasswordResetConfirmView

urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('redirect/',views.NewLogin,name='my_account'),
    path('',views.MainPage,name='main_page'),
    path('courses/add_new_course/',views.addCourse,name='add_course'),
    path('courses/register/',views.registerCourse,name='register_course'),
    path('courses/<str:name>/',views.coursePage,name='course_page'),
    path('courses/<str:name>/members',views.courseMembers,name='course_members'),    #dhvanit
    path('courses/<str:name>/forum',views.courseForum,name='course_forum'),    #dhvanit
    path('courses/<str:name>/forum/disable',views.disableForum,name='disable_forum'),    #dhvanit
    path('courses/<str:name>/forum/enable',views.enableForum,name='enable_forum'),    #dhvanit
    path('users/dm/<str:username>',views.directMessage,name='direct_message'),    #dhvanit
    path('users/<str:username>/',views.profilePage,name='profile_page'),
    path('courses/<str:name>/add_new_assignment/',views.addAssign,name='add_assign'),
    path('courses/<str:name>/assignment/<int:id>/',views.viewAssign,name='view_assign'),
    path('changepass/',views.PasswordChangeView.as_view(),name='change_password'),
    path('reset_password/',PasswordResetView.as_view(),name='password_reset'), #dhvanit
    path('reset_password/done',PasswordResetDoneView.as_view(),name='password_reset_done'), #dhvanit
    path('reset_password/confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'), #dhvanit
    path('reset_password/complete',PasswordResetCompleteView.as_view(),name='password_reset_complete'), #dhvanit
    path('updateprofile/',views.changeUserProfile,name='updateProfile'),
    path('courses/<str:name>/assignment/<int:id>/upload_csv',views.CsvFeedbackView,name='upload_csv')
]