
from django.http import response
from django.urls.base import reverse
from django.contrib.auth.models import User
from userprofile.models import Course, CourseUserRelation
from userprofile.signup import SignUpForm
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from datetime import datetime, time,timedelta, tzinfo
# Create your views here.

class SignUpView(generic.CreateView):
    template_name='registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

def NewLogin(request):
    return redirect(reverse('main_page',kwargs={'username':request.user.username}))


def MainPage(request,username):
    if(User.is_authenticated):
        current_user=request.user
        all_users=User.objects.all()
        logged_in_users=[]
        for user in all_users:
            if(user==current_user):
                continue
            time=user.last_login
            if(datetime.now()<time.replace(tzinfo=None)+timedelta(minutes=5)):    #timestamp with timezone problem
                logged_in_users.append(user)
        all_courses=Course.objects.all()
        course_relation=CourseUserRelation.objects.filter(user_id=current_user.pk)
        course_ids=[]
        for relation in course_relation:
            course_ids.append(relation.course_id)
        available_courses=[]
        learner_courses=[]
        teacher_courses=[]
        for course in all_courses:
            index=course_ids.index(course.pk) if course.pk in course_ids else None
            if(index==None):
                available_courses.append(course)
            else:
                if(course_relation[index].is_student):
                    learner_courses.append(course)
                elif(course_relation[index].is_teacher):
                    teacher_courses.append(course)
        contents={
            "available_courses":available_courses,
            "learner_courses":learner_courses,
            "teacher_courses":teacher_courses,
            "logged_in_users":logged_in_users
        }
        return render(request,'mainpage.html',contents)




