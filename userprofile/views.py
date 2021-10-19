
from django.http import response
from django.urls.base import reverse
from django.contrib.auth.models import User
import userprofile
from userprofile.models import Assignments, Course, CourseUserRelation, Lecture, LectureNotes, Solutions, Solutionfeedback
from userprofile.signup import SignUpForm
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from datetime import datetime, time,timedelta, tzinfo
from .forms import CourseCreationForm, CourseRegistrationForm, LectureCreationForm, AssignmentCreationForm, SolutionSubmissionForm, SolutionFeedbackForm
# Create your views here.

class SignUpView(generic.CreateView):
    template_name='registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

def NewLogin(request):
    return redirect(reverse('main_page'))


def MainPage(request):
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
        learner_courses=[]      #course_id[1]   course_relation[1]
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

def addCourse(request):
    if request.method == 'POST':
        form = CourseCreationForm(request.POST)
        if form.is_valid():
            newCourse = Course.objects.create(name = form.cleaned_data['name'], color = form.cleaned_data['color'], code = form.cleaned_data['code'])
            newCourse.save()
            newCourse.user.add(request.user)
            CourseUserRelation.objects.create(user = request.user, course = newCourse, is_teacher = True)
            return redirect(reverse('main_page'))
        else:
            return redirect(reverse('add_course'))
    else:
        form = CourseCreationForm()
    return render(request,'addCourse.html', {'form':form})

def registerCourse(request):
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            newCourse = Course.objects.get(name=form.cleaned_data['Course_name'])
            if newCourse.code==form.cleaned_data['Course_code'] :
                newCourse.user.add(request.user)
                CourseUserRelation.objects.create(user=request.user, course=newCourse, is_student = True)
            else:
                return redirect(reverse('register_course'))
            return redirect(reverse('main_page'))
        else:
            return redirect(reverse('register_course'))
    else:
        form = CourseRegistrationForm()
    return render(request,'registerCourse.html', {'form':form})

def coursePage(request, name):
    relation = CourseUserRelation.objects.filter(user=request.user).get(course__name=name)
    course = Course.objects.get(name=name)
    lectures = relation.course.lecture_set.all()
    assignments = course.assignments_set.all()
    if request.method == 'POST':
        form = LectureCreationForm(request.POST, request.FILES)
        if form.is_valid():
            newLecture = Lecture.objects.create(course=course, title = form.cleaned_data['title'], description=form.cleaned_data['description'])
            notes = LectureNotes.objects.create(lecture=newLecture, file=request.FILES['notes'])
            return redirect(reverse('course_page', kwargs={'name':name}))
        else:
            return redirect(reverse('course_page', kwargs={'name':name}))
    else:
        form = LectureCreationForm()
    args = {
        'relation':relation,
        'lectures':lectures,
        'assignments':assignments,
        'form':form,
        'course':course
    }
    return render(request, 'coursePage.html', args)

def addAssign(request,name):
    course = Course.objects.get(name=name)
    if request.method == 'POST':
        form = AssignmentCreationForm(request.POST, request.FILES)
        if form.is_valid():
            newAssignment = Assignments.objects.create(
                course=course,
                prob_description=form.cleaned_data['p_description'],
                problemfile=request.FILES['Problem'],
                deadline=form.cleaned_data['Deadline']
            )
            
            return redirect(reverse('course_page', kwargs={'name':name}))
        else:
            return redirect(reverse('add_assign', kwargs={'name':name}))
    else:
        form = AssignmentCreationForm()
    return render(request,'addAssign.html', {'form':form})

def viewAssign(request,name,id):
    course = Course.objects.get(name=name)
    assignment = Assignments.objects.get(pk=id)
    relation = CourseUserRelation.objects.filter(user=request.user).get(course__name=name)
    if(relation.is_student):
        if request.method == 'POST':
            form = SolutionSubmissionForm(request.POST,request.FILES)
            if form.is_valid():
                Solutions.objects.update_or_create(student=request.user, assignment=assignment, defaults={'solutionfile':request.FILES['solutionfile']})
                return redirect(reverse('view_assign', kwargs={'name':name,'id':id}))
            else:
                return redirect(reverse('view_assign', kwargs={'name':name,'id':id}))
        else:
            form = SolutionSubmissionForm()
        solutions=Solutions.objects.filter(student=request.user, assignment=assignment)
    else:
        if request.method == 'POST':
            for solution in assignment.solutions_set.all():
                if f"{solution.student.pk}" in request.POST:
                    form = SolutionFeedbackForm(request.POST)
                    if form.is_valid():
                        if Solutionfeedback.objects.filter(solution=solution).exists():
                            obj = Solutionfeedback.objects.get(solution=solution)
                            obj.feedback = form.cleaned_data['feedback']
                            obj.save()
                        else:
                            Solutionfeedback.objects.create(solution=solution,feedback=form.cleaned_data['feedback'])
                        #Solutionfeedback.objects.update_or_create(solution=solution,feedback=form.cleaned_data['feedback'])
                        return redirect(reverse('view_assign', kwargs={'name':name,'id':id}))
                    else:
                        return redirect(reverse('view_assign', kwargs={'name':name,'id':id}))
        else:
            form = SolutionFeedbackForm()
        solutions=Solutions.objects.filter(assignment=assignment)
    args = {
        'form':form,
        'solutions':solutions,
        'assignment':assignment,
        'relation':relation
    }
    return render(request,'viewAssign.html', args)

def profilePage(request, username):
    user = User.objects.get(username=username)
    courses = Course.objects.filter(user=user)
    args = {
        'user':user,
        'courses':courses
    }
    return render(request, 'profilePage.html', args)