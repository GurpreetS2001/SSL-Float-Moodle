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
    path('changepass/',views.PasswordChangeView.as_view(),name='change_password'),
    path('updateprofile/',views.changeUserProfile,name='updateProfile'),
    path('courses/<str:name>/assignment/<int:id>/upload_csv/',views.CsvFeedbackView,name='upload_csv'),
    path('courses/<str:name>/student/course_stats/',views.StudentCourseStats,name="student_course_stats"),
    path('courses/<str:name>/assignment/<int:id>/stats/',views.TeacherAssignmentStats,name="assignment_stats"),
    path('courses/<str:name>/teacher/course_stats/',views.TeacherCourseStats,name="teacher_course_stats"),
    path('courses/<str:name>/<str:lecture_num>/',views.coursePage,name='course_page'),
]