

from typing import OrderedDict  #dhvanit
from django.conf import settings    #dhvanit
from django.core.mail import send_mail
from django.http import response
from django.urls.base import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
import userprofile
import csv
import json
from django.contrib import messages
from userprofile.models import *
from userprofile.signup import SignUpForm
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from datetime import datetime, time,timedelta, tzinfo
from .forms import *
from .aggregates import CalculateCourseMarksStudent, CalculatePercentageCourseCompleted, GenerateTeacherStatsAssignment, GenerateTeacherStatsCourse, ToDoListStudent
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
            if(not time):   #case arises when an account was signed up but never logged in #dhvanit
                continue    #dhvanit
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
                elif(course_relation[index].is_teacher or course_relation[index].is_TA):
                    teacher_courses.append(course)
        print('-----------')
        print(logged_in_users)
        print('-----------')
        toDoListStudents=ToDoListStudent(current_user)
        learner_courses=CalculatePercentageCourseCompleted(learner_courses,request.user)
        contents={
            "available_courses":available_courses,
            "learner_courses":learner_courses,
            "teacher_courses":teacher_courses,
            "logged_in_users":logged_in_users,
            "toDoStudent":toDoListStudents
        }
        return render(request,'mainpage.html',contents)

def addCourse(request):
    if request.method == 'POST':
        form = CourseCreationForm(request.POST)
        if form.is_valid():
            newCourse = Course.objects.create(  #/dhvanit
                name = form.cleaned_data['Course_name'], color = '#007bff',
                code = form.cleaned_data['Course_code'],
                regcode_student = form.cleaned_data['regcode_student'],
                regcode_TA = form.cleaned_data['regcode_TA']
                ) 
            newCourse.save()
            newCourse.user.add(request.user)
            CourseUserRelation.objects.create(user = request.user, course = newCourse, is_teacher = True)
            Privileges.objects.create(user=request.user, course=newCourse, can_grade=True, can_create_assignments=True, can_create_lectures=True)   #dhvanit
            #/dhvanit
            if form.cleaned_data['email_invites']:
                recipient_list = []
                for user in User.objects.all():
                    recipient_list.append(user.email)
                send_mail('New Public course',f"A new public course was created titled \'{newCourse.name}\' ({newCourse.code}). Join with registration code {newCourse.regcode_student}",settings.EMAIL_HOST_USER,recipient_list)
                #dhvanit/
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
                if form.cleaned_data['Registration_code']==newCourse.regcode_student :  #/dhvanit
                    CourseUserRelation.objects.create(user=request.user, course=newCourse, is_student = True)
                    Privileges.objects.create(user=request.user, course=newCourse)
                elif form.cleaned_data['Registration_code']==newCourse.regcode_TA :
                    CourseUserRelation.objects.create(user=request.user, course=newCourse, is_TA = True)
                    Privileges.objects.create(user=request.user, course=newCourse, can_grade=True, can_create_assignments=False, can_create_lectures=False)
                else:
                    return redirect(reverse('register_course'))
            else:
                return redirect(reverse('register_course'))
            return redirect(reverse('main_page'))
        else:
            return redirect(reverse('register_course'))
    else:
        form = CourseRegistrationForm()
    return render(request,'registerCourse.html', {'form':form})

def coursePage(request, name , lecture_num):
    relation = CourseUserRelation.objects.filter(user=request.user).get(course__name=name)
    privileges = Privileges.objects.filter(user=request.user).get(course__name=name) 
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
        'privileges':privileges,
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
            course_members = CourseUserRelation.objects.filter(course__name=name)   #/dhvanit
            recipient_list = []
            for relation in course_members:
                recipient_list.append(relation.user.email)
            send_mail('New Assignment',f"A new assignment has been uploaded for the course {course.name} ({course.code})",settings.EMAIL_HOST_USER,recipient_list)  #dhvanit/
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
    privileges = Privileges.objects.filter(user=request.user).get(course__name=name)
    past_deadline = (datetime.now()>assignment.deadline)
    if(relation.is_student):
        if request.method == 'POST':
            form = SolutionSubmissionForm(request.POST,request.FILES)
            if form.is_valid():
                Solutions.objects.update_or_create(student=request.user, assignment=assignment, defaults={'solutionfile':request.FILES['solutionfile']})
                send_mail('Successful submission',f"Hi {request.user.username}, your submission was done successfully",settings.EMAIL_HOST_USER,[request.user.email])    #dhvanit
                return redirect(reverse('view_assign', kwargs={'name':name,'id':id}))
            else:
                return redirect(reverse('view_assign', kwargs={'name':name,'id':id}))
        else:
            form = SolutionSubmissionForm()
        solutions=Solutions.objects.filter(student=request.user, assignment=assignment)
    elif(privileges.can_grade): #dhvanit
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
    else:   #/dhvanit
        form = None
        solutions = []
    download_links=[]
    for solution in solutions:
        download_links.append(solution.solutionfile.url)
    json_links=json.dumps(download_links)
    submission_exists=False
    try:
        sol=Solutions.objects.filter(assignment=assignment).get(student=request.user)
        submission_exists=True
    except Solutions.DoesNotExist:
        pass
    args = {
        'privileges':privileges,
        'form':form,
        'solutions':solutions,
        'assignment':assignment,
        'relation':relation,
        'course':course,
        'json_links':json_links,
        'past_deadline':past_deadline,
        'submission_exists':submission_exists
    }
    return render(request,'viewAssign.html', args)

def profilePage(request, username):
    current_user=request.user
    user = User.objects.get(username=username)
    courses = Course.objects.filter(user=user)
    all_courses=Course.objects.all()
    course_relation=CourseUserRelation.objects.filter(user_id=user.pk)
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
            elif(course_relation[index].is_teacher or course_relation[index].is_TA):    #dhvanit
                teacher_courses.append(course)
    args = {
        'user':current_user,    #dhvanit
        'visiting_user':user,
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
        try:
            if CourseUserRelation.objects.filter(course=course).get(user=request.user).is_student:
                student_assignmentwise_stats,total_marks,percentage_score,max_marks,max_percentage=CalculateCourseMarksStudent(course,request.user)
                args={
                    'course':course,
                    'assignmentwise_stats':student_assignmentwise_stats,
                    'total_marks':total_marks,
                    'percentage_score':percentage_score,
                    'max_marks':max_marks,
                    'max_percentage':max_percentage
                }
                return render(request,'student_stats.html',args)
            else:
                return response.HttpResponse('Teacher hai bhai tu')
        except CourseUserRelation.DoesNotExist:
            return response.HttpResponse('Register toh karle bhai')
    else:
        redirect(reverse('login'))    
        
def TeacherAssignmentStats(request,name,id):
    if request.user.is_authenticated:
        course=Course.objects.get(name=name)
        assignment=Assignments.objects.filter(course=course).get(pk=id)
        mean,variance,scatter_url,hist_url=GenerateTeacherStatsAssignment(course,assignment)
        args={
            'assignment':assignment,
            'course':course,
            'mean':mean,
            'variance':variance,
            'scatter_url':scatter_url,
            'hist_url':hist_url
        }
        return render(request,'assignment_stats.html',args)



def TeacherCourseStats(request,name):
    if request.user.is_authenticated:
        course=Course.objects.get(name=name)
        assignments=Assignments.objects.filter(course=course)
        all_students,total_score_list,percent_score_list,score_histogram_url,percent_histogram_url,stats,max_marks,marks_percentage=GenerateTeacherStatsCourse(course)
        students_data=list(zip(all_students,total_score_list,percent_score_list))
        args={
            'course':course,
            'students_data':students_data,
            'score_hist_url':score_histogram_url,
            'per_hist_url':percent_histogram_url,
            'assignments':assignments,
            'stats':stats,
            'max_marks':max_marks,
            'max_percentage':marks_percentage
        }
        return render(request,'course_stats.html',args)
    else:
        redirect(reverse('login'))

def courseMembers(request, name):   #/dhvanit
    course = Course.objects.get(name=name)
    relation = CourseUserRelation.objects.filter(user=request.user).get(course__name=name)
    all_users = CourseUserRelation.objects.filter(course__name=name)
    students=[]
    tas=[]
    for user in all_users:
        if user.is_student:
            students.append(user)
        elif user.is_TA:
            tas.append(user)
    if request.method == 'POST':
        form = SetTAPrivilegesForm(request.POST)
        if form.is_valid():
            for ta in tas:
                privileges = Privileges.objects.filter(user=ta.user).get(course__name=name)
                privileges.can_grade = form.cleaned_data['can_grade']
                privileges.can_create_assignments = form.cleaned_data['can_create_assignments']
                privileges.can_create_lectures = form.cleaned_data['can_create_lectures']
                privileges.save()
            return redirect(reverse('course_members', kwargs={'name':name}))
        else:
            return redirect(reverse('course_members', kwargs={'name':name}))
    else:
        if len(tas)>0:
            privileges = Privileges.objects.filter(user=tas[0].user).get(course__name=name)
            initial = {'can_grade':privileges.can_grade, 'can_create_assignments':privileges.can_create_assignments, 'can_create_lectures':privileges.can_create_lectures}
            form = SetTAPrivilegesForm(initial)
        else:
            form = SetTAPrivilegesForm()
    args = {
        'relation':relation,
        'students':students,
        'tas':tas,
        'course':course,
        'form':form
    }
    return render(request, 'courseMembers.html', args)

def courseForum(request,name):
    course = Course.objects.get(name=name)
    questions = course.forumquestions_set.all().order_by('-created_at')
    answers = OrderedDict()    #dict with (key, value) being (question, answer_set)
    for question in questions:
        answers[question] = question.forumanswers_set.all().order_by('created_at')
        print(question,answers[question])
    if request.method == 'POST':
        for question in questions:
            if f"{question.pk}" in request.POST:
                aform = ForumAnswerForm(request.POST)
                qform = ForumQuestionForm()
                if aform.is_valid():
                    ForumAnswers.objects.create(question=question,user=request.user,content=aform.cleaned_data['content'])
                    return redirect(reverse('course_forum', kwargs={'name':name}))
                else:
                    return redirect(reverse('course_forum', kwargs={'name':name}))
        if "asked_question" in request.POST:
            qform = ForumAnswerForm(request.POST)
            aform = ForumAnswerForm()
            if qform.is_valid():
                ForumQuestions.objects.create(course=course,user=request.user,content=qform.cleaned_data['content'])
                return redirect(reverse('course_forum', kwargs={'name':name}))
            else:
                return redirect(reverse('course_forum', kwargs={'name':name}))
        else:
            return redirect(reverse('course_forum', kwargs={'name':name}))
    else:
        qform = ForumQuestionForm()
        aform = ForumAnswerForm()
    args = {
        'course':course,
        'questions':questions,
        'answers':answers,
        'qform':qform,
        'aform':aform
    }
    return render(request, 'courseForum.html', args)

def disableForum(request,name):
    course = Course.objects.get(name=name)
    course.forums_enabled = False
    course.save()
    return redirect(reverse('course_page', kwargs={'name':name}))

def enableForum(request,name):
    course = Course.objects.get(name=name)
    course.forums_enabled = True
    course.save()
    return redirect(reverse('course_page', kwargs={'name':name})) 

def directMessage(request, username):   #/dhvanit
    user = request.user
    user2 = User.objects.get(username=username)
    sent_messages = DirectMessage.objects.filter(sender=user).filter(receiver=user2)
    received_messages = DirectMessage.objects.filter(sender=user2).filter(receiver=user)
    all_messages = (sent_messages|received_messages).order_by('sent_at')
    if request.method=="POST":
        form = DirectMessageForm(request.POST)
        if form.is_valid():
            DirectMessage.objects.create(sender=user,receiver=user2,content=form.cleaned_data['content'])
            send_mail('New message',f"Hi {user2.username}, you have received a new message from {user.username}",settings.EMAIL_HOST_USER,[user2.email])
            return redirect(reverse('direct_message', kwargs={'username':username}))
        else:
            return redirect(reverse('direct_message', kwargs={'username':username}))
    else:
        form = DirectMessageForm()
    args={
        'user':user,
        'user2':user2,
        'all_messages':all_messages,
        'form':form
    }
    return render(request, 'directMessage.html', args)  #dhvanit/