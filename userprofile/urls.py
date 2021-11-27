from userprofile import views
from django.urls import path,include
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetCompleteView,PasswordResetConfirmView
from . import views

urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('redirect/',views.NewLogin,name='my_account'),
    path('',views.MainPage,name='main_page'),
    path('courses/add_new_course/',views.addCourse,name='add_course'),
    path('courses/register/',views.registerCourse,name='register_course'),
    path('users/direct_message/',views.seeDMlist,name='dm_list'),    #dhvanit
    path('users/<str:username>/',views.profilePage,name='profile_page'),
    path('courses/<str:name>/add_new_assignment/',views.addAssign,name='add_assign'),
    path('courses/<str:name>/assignment/<int:id>/',views.viewAssign,name='view_assign'),
    ####
    path('courses/<str:name>/members',views.courseMembers,name='course_members'),    #dhvanit
    path('courses/<str:name>/forum',views.courseForum,name='course_forum'),    #dhvanit
    path('courses/<str:name>/forum/disable',views.disableForum,name='disable_forum'),    #dhvanit
    path('courses/<str:name>/forum/enable',views.enableForum,name='enable_forum'),    #dhvanit
    
    path('users/direct_message/<str:username>',views.directMessage,name='direct_message'), #dhvanit
    path('reset_password/',PasswordResetView.as_view(),name='password_reset'), #dhvanit
    path('reset_password/done',PasswordResetDoneView.as_view(),name='password_reset_done'), #dhvanit
    path('reset_password/confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'), #dhvanit
    path('reset_password/complete',PasswordResetCompleteView.as_view(),name='password_reset_complete'), #dhvanit
    path('changepass/',views.PasswordChangeView.as_view(),name='change_password'),
    path('updateprofile/',views.changeUserProfile,name='updateProfile'),
    path('courses/<str:name>/assignment/<int:id>/upload_csv/',views.CsvFeedbackView,name='upload_csv'),
    path('courses/<str:name>/student/course_stats/',views.StudentCourseStats,name="student_course_stats"),
    path('courses/<str:name>/assignment/<int:id>/stats/',views.TeacherAssignmentStats,name="assignment_stats"),
    path('courses/<str:name>/teacher/course_stats/',views.TeacherCourseStats,name="teacher_course_stats"),
    path('courses/<str:name>/<str:lecture_num>/',views.coursePage,name='course_page'),
    
]