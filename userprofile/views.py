from django.http import response
from django.urls.base import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
import userprofile
import csv
import json
from django.contrib import messages
from userprofile.models import Assignments, Course, CourseUserRelation, CsvFeedback, Lecture, LectureNotes, Solutions, Solutionfeedback,LectureCompleted
from userprofile.signup import SignUpForm
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from datetime import datetime, time,timedelta, tzinfo
from .forms import ChangePasswordForm, ChangeUserProfileForm, CourseCreationForm, CourseRegistrationForm, CsvFeedbackSubmissionForm, LectureCompletionForm, LectureCreationForm, AssignmentCreationForm, SolutionSubmissionForm, SolutionFeedbackForm
from .aggregates import CalculateCourseMarksStudent, CalculatePercentageCourseCompleted, GenerateTeacherStatsAssignment, GenerateTeacherStatsCourse
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
            print(datetime.now())
            print(time)
            print(timedelta(minutes=5))
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
        print('-----------')
        print(logged_in_users)
        print('-----------')
        contents={
            "available_courses":available_courses,
            "learner_courses":CalculatePercentageCourseCompleted(learner_courses,request.user),
            "teacher_courses":teacher_courses,
            "logged_in_users":logged_in_users,
        }
        return render(request,'mainpage.html',contents)

def addCourse(request):
    if request.method == 'POST':
        form = CourseCreationForm(request.POST)
        if form.is_valid():
            newCourse = Course.objects.create(name = form.cleaned_data['name'], color = '#007bff', code = form.cleaned_data['code'])
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

def coursePage(request, name , lecture_num=-1):
    relation = CourseUserRelation.objects.filter(user=request.user).get(course__name=name)
    course = Course.objects.get(name=name)
    lectures_content = relation.course.lecture_set.all()
    assignments = course.assignments_set.all()
    lectures=[]
    ######
    if request.method == 'POST':
        if 'Upload' in request.POST:
            form = LectureCreationForm(request.POST, request.FILES)
            #lc_form = LectureCompletionForm()
            if form.is_valid():
                newLecture = Lecture.objects.create(course=course, title = form.cleaned_data['title'], description=form.cleaned_data['description'])
                notes = LectureNotes.objects.create(lecture=newLecture, file=request.FILES['notes'])
                return redirect(reverse('course_page', kwargs={'name':name,'lecture_num':"-1"}))
            else:
                return redirect(reverse('course_page', kwargs={'name':name,'lecture_num':"-1"}))
        elif 'lec_incomplete' in request.POST:
            # lc_form = LectureCompletionForm(request.POST)
            # #form = LectureCreationForm()
            # if lc_form.is_valid():
            lecture_num=int(lecture_num)
            lecture=Lecture.objects.get(pk=lecture_num)
                #lec_object=LectureCompleted.objects.update_or_create(lecture=lecture,user=request.user,lecture_completed=lc_form.cleaned_data['lecture_completed'])
            #if LectureCompleted.objects.filter(lecture=lecture).get(user=request.user).exists():
            try:
                lec_completed=LectureCompleted.objects.filter(lecture=lecture).get(user=request.user)
                lec_completed.lecture_completed=True
                lec_completed.save()
            except LectureCompleted.DoesNotExist:
                LectureCompleted.objects.create(lecture=lecture,user=request.user,lecture_completed=True)
            return redirect(reverse('course_page', kwargs={'name':name,'lecture_num':"-1"}))
        elif 'lec_completed' in request.POST:
            lecture_num=int(lecture_num)
            lecture=Lecture.objects.get(pk=lecture_num)
                #lec_object=LectureCompleted.objects.update_or_create(lecture=lecture,user=request.user,lecture_completed=lc_form.cleaned_data['lecture_completed'])
            # if LectureCompleted.objects.filter(lecture=lecture).get(user=request.user)!=:
            try:
                lec_completed=LectureCompleted.objects.filter(lecture=lecture).get(user=request.user)
                lec_completed.lecture_completed=False
                lec_completed.save()
            except LectureCompleted.DoesNotExist:
                LectureCompleted.objects.create(lecture=lecture,user=request.user,lecture_completed=False)
            return redirect(reverse('course_page', kwargs={'name':name,'lecture_num':"-1"}))
    else:
        form = LectureCreationForm()
        for lecture in lectures_content:
            # if LectureCompleted.objects.filter(lecture=lecture).exists():
            try:
                completed=LectureCompleted.objects.filter(lecture=lecture).get(user=request.user).lecture_completed
                lectures.append([lecture,completed])
            except LectureCompleted.DoesNotExist:
                lectures.append([lecture,False])
    print(lectures)
    args = {
        'relation':relation,
        'lectures':lectures,
        'assignments':assignments,
        'form':form,
        'course':course
    }
    #####
    return render(request, 'coursePage.html', args)

def addAssign(request,name):
    course = Course.objects.get(name=name)
    if request.method == 'POST':
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        form = AssignmentCreationForm(request.POST, request.FILES)
        if form.is_valid():
            newAssignment = Assignments.objects.create(
                course=course,
                prob_description=form.cleaned_data['p_description'],
                problemfile=request.FILES['Problem'],
                deadline=form.cleaned_data['Deadline'],
                #####
                max_marks = form.cleaned_data['max_marks'],
                course_weightage = form.cleaned_data['course_weightage'],
                assignment_name=form.cleaned_data['assignment_name']
            )
            return redirect(reverse('course_page', kwargs={'name':name,'lecture_num':"-1"}))
        else:
            return redirect(reverse('add_assign', kwargs={'name':name}))
    else:
        form = AssignmentCreationForm()
    return render(request,'addAssign.html', {'form':form,'course':course})

def viewAssign(request,name,id):
    course = Course.objects.get(name=name)
    assignment = Assignments.objects.get(pk=id)
    relation = CourseUserRelation.objects.filter(user=request.user).get(course__name=name)
    past_deadline = (datetime.now()>assignment.deadline)
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
                            #####
                            obj.marks_obtained = form.cleaned_data['marks_obtained']
                            #####
                            obj.save()
                        else:
                            ######
                            Solutionfeedback.objects.create(solution=solution,feedback=form.cleaned_data['feedback'],marks_obtained=form.cleaned_data['marks_obtained'])
                            ######
                        #Solutionfeedback.objects.update_or_create(solution=solution,feedback=form.cleaned_data['feedback'])
                        return redirect(reverse('view_assign', kwargs={'name':name,'id':id}))
                    else:
                        return redirect(reverse('view_assign', kwargs={'name':name,'id':id}))
        else:
            form = SolutionFeedbackForm()
        solutions=Solutions.objects.filter(assignment=assignment)
    download_links=[]
    for solution in solutions:
        download_links.append("http://127.0.0.1:8000"+solution.solutionfile.url)
    json_links=json.dumps(download_links)
    submission_exists=False
    try:
        sol=Solutions.objects.filter(assignment=assignment).get(student=request.user)
        submission_exists=True
    except Solutions.DoesNotExist:
        pass
    args = {
        'form':form,
        'solutions':solutions,
        'assignment':assignment,
        'relation':relation,
        'course':course,
        'json_links':json_links,
        'past_deadline':past_deadline,
        'submission_exists':submission_exists,
    }
    return render(request,'viewAssign.html', args)

def profilePage(request, username):
    current_user=request.user
    user = User.objects.get(username=username)
    courses = Course.objects.filter(user=user)
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
    args = {
        'user':user,
        'courses':courses,
        "available_courses":available_courses,
        "learner_courses":learner_courses,
        "teacher_courses":teacher_courses,

    }
    return render(request, 'profilePage.html', args)

class PasswordChangeView(PasswordChangeView):
    template_name = 'changepassword.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('main_page')

def changeUserProfile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            rec_form=ChangeUserProfileForm(request.POST,instance=request.user)
            if rec_form.is_valid():
                messages.success(request,'Profile Updated')
                rec_form.save()
        else:
            rec_form=ChangeUserProfileForm(instance=request.user)
        return render(request,'updateProfile.html',{'form':rec_form})
    else:
        return response.HttpResponse('Login First')

def CsvFeedbackView(request,name,id):
    assignment = Assignments.objects.get(pk=id)
    if request.method == "POST":
        form = CsvFeedbackSubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            csv_obj = CsvFeedback.objects.create(assignment=assignment,feedback_csv=request.FILES['feedback_csv'])
            with open(csv_obj.feedback_csv.path,'r') as csv_file:
                reader = csv.reader(csv_file)

                for i,row in enumerate(reader):
                    if i==0:
                        pass
                    else:
                        if User.objects.filter(username=row[0]).exists():
                            student=User.objects.get(username=row[0])
                            solution = Solutions.objects.filter(student=student,assignment=assignment)
                            if Solutionfeedback.objects.filter(solution=solution[0]).exists:
                                ######
                                solution_feedback_object = Solutionfeedback.objects.get(solution=solution[0])
                                solution_feedback_object.feedback=",".join(row[1:-1])
                                solution_feedback_object.marks_obtained=float(row[-1])
                                solution_feedback_object.save()
                            else:
                                solution_feedback_object = Solutionfeedback.objects.create(solution=solution[0],feedback=",".join(row[1:-1]),marks_obtained=float(row[-1]))
                                #######
            csv_obj.active=False
            csv_obj.save()
            return redirect(reverse('view_assign', kwargs={'name':name,'id':id}))
    else:
        form =CsvFeedbackSubmissionForm()
        return render(request,'csvfeedback.html',{'form':form})


def StudentCourseStats(request,name):
    if request.user.is_authenticated:
        course=Course.objects.get(name=name)
        if CourseUserRelation.objects.filter(course=course).get(user=request.user).is_student:
            student_assignmentwise_stats,total_marks,percentage_score=CalculateCourseMarksStudent(course,request.user)
            args={
                'course':course,
                'assignmentwise_stats':student_assignmentwise_stats,
                'total_marks':total_marks,
                'percentage_score':percentage_score
            }
            return render(request,'student_stats.html',args)
        else:
            return response.HttpResponse('Teacher hai bhai tu')
    else:
        redirect(reverse('login'))    
        
def TeacherAssignmentStats(request,name,id):
    if request.user.is_authenticated:
        course=Course.objects.get(name=name)
        assignment=Assignments.objects.filter(course=course).get(pk=id)
        mean,variance,scatter_url,hist_url=GenerateTeacherStatsAssignment(course,assignment)
        args={
            'mean':mean,
            'variance':variance,
            'scatter_url':scatter_url,
            'hist_url':hist_url
        }
        return render(request,'assignment_stats.html',args)



def TeacherCourseStats(request,name):
    if request.user.is_authenticated:
        course=Course.objects.get(name=name)
        all_students,total_score_list,percent_score_list,score_histogram_url,percent_histogram_url=GenerateTeacherStatsCourse(course)
        students_data=list(zip(all_students,total_score_list,percent_score_list))
        args={
            'students_data':students_data,
            'score_hist_url':score_histogram_url,
            'per_hist_url':percent_histogram_url
        }
        return render(request,'course_stats.html',args)
    else:
        redirect(reverse('login')) 