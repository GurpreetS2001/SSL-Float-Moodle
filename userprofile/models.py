from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL 
from embed_video.fields import EmbedVideoField
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=CASCADE)
    image=models.ImageField(upload_to='profile_photo',default='default.jpg')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=50,primary_key=True)
    color = models.CharField(max_length=7,default='#007bff')
    user = models.ManyToManyField(User)  #not sure about on_delete
    code = models.CharField(max_length=10,null=True)
    regcode_student = models.CharField(max_length=10,null=True) #dhvanit
    regcode_TA = models.CharField(max_length=10,null=True)  #dhvanit
    forums_enabled = models.BooleanField(default = True)

    def __str__(self):
        return self.name

class Privileges(models.Model): #/dhvanit
    user = models.ForeignKey(User,on_delete=CASCADE)
    course = models.ForeignKey(Course,on_delete=CASCADE)
    can_grade = models.BooleanField(default = False)
    can_create_assignments = models.BooleanField(default = False)
    can_create_lectures = models.BooleanField(default = False)

class ForumQuestions(models.Model):
    course = models.ForeignKey(Course,on_delete=CASCADE)
    user = models.ForeignKey(User,default=None,on_delete=CASCADE)   #can remove default I think
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)

class ForumAnswers(models.Model):
    question = models.ForeignKey(ForumQuestions,on_delete=CASCADE)
    user = models.ForeignKey(User,default=None,on_delete=CASCADE)   #can remove default I think
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=CASCADE, related_name='receiver')
    sent_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True) 


class CourseUserRelation(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    course = models.ForeignKey(Course,on_delete=CASCADE)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_TA = models.BooleanField(default = False)  

    
class Lecture(models.Model):
    course = models.ForeignKey(Course,on_delete=CASCADE)
    # user= models.ForeignKey(User,on_delete=CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    video = EmbedVideoField(blank=True, null=True)

    def __str__(self):
        return self.title


class LectureNotes(models.Model):
    lecture = models.OneToOneField(Lecture,on_delete=CASCADE)
    file = models.FileField(upload_to='notes',null=True,blank=True)

#####
class LectureCompleted(models.Model):
    lecture = models.ForeignKey(Lecture,on_delete=CASCADE)
    user = models.ForeignKey(User,on_delete=CASCADE)
    lecture_completed = models.BooleanField(default=False)
#####

class Assignments(models.Model):
    course = models.ForeignKey(Course,on_delete=CASCADE)
    assignment_name = models.CharField(max_length=100)
    prob_description = models.TextField(blank=True)
    problemfile = models.FileField(upload_to='assignments/problem',null=True,blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    #####
    max_marks = models.FloatField()
    course_weightage = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    ##### 
    #Assignment Solution Model
    def __str__(self):
        return self.course.name

class Solutions(models.Model):
    student=models.ForeignKey(User,on_delete=CASCADE)
    assignment=models.ForeignKey(Assignments,on_delete=CASCADE)
    solutionfile = models.FileField(upload_to='assignments/solutions',null=True,blank=True)
    submission_time = models.DateTimeField(auto_now=True)

class Solutionfeedback(models.Model):
    solution=models.OneToOneField(Solutions,on_delete=CASCADE)
    feedback = models.TextField(blank=True)
    #####
    marks_obtained = models.FloatField(default=0.0)
    #####

class Quiz(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    course = models.ForeignKey(Course,on_delete=CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    quiz_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_marks = models.IntegerField()
    marks_obtained = models.IntegerField()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=CASCADE)   #explore related_name
    prob_description = models.TextField()
    prob_file = models.FileField(upload_to=f"{quiz.name}/quizzes")
    #how to take mcqs?

class Answer(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=CASCADE)
    ques = models.ForeignKey(Question,on_delete=CASCADE)
    solution_text = models.TextField()
    solutionFile = models.FileField(upload_to=f"{quiz.name}/quiz_answers")

class CsvFeedback(models.Model):
    assignment = models.ForeignKey(Assignments,on_delete=CASCADE)
    feedback_csv = models.FileField(upload_to='assignments/csv',null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    active = models.BooleanField(default=True)