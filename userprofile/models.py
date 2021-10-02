from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL 
from embed_video.fields import EmbedVideoField
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

    def __str__(self):
        return self.name


class CourseUserRelation(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    course = models.ForeignKey(Course,on_delete=CASCADE)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

    
class Lecture(models.Model):
    course = models.ForeignKey(Course,on_delete=CASCADE)
    user= models.ForeignKey(User,on_delete=CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    video = EmbedVideoField(blank=True, null=True)

    def __str__(self):
        return self.title


class LectureNotes(models.Model):
    lecture = models.OneToOneField(Lecture,on_delete=CASCADE)
    file = models.FileField(upload_to='notes',null=True,blank=True)


class Assignments(models.Model):
    course = models.ForeignKey(Course,on_delete=CASCADE)
    prob_description = models.TextField(blank=True)
    problemfile = models.FileField(upload_to=f"{course.name}/problem",null=True,blank=True)
    solutionfile = models.FileField(upload_to=f"{course.name}/problem",null=True,blank=True)
    sol_description = models.TextField(blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    submission_time = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField() 

    def __str__(self):
        return self.course.name

class Quiz(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    course = models.ForeignKey(Course,on_delete=CASCADE)
    name = models.CharField(max_length=100)
    quiz_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_marks = models.IntegerField()
    marks_obtained = models.IntegerField()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=CASCADE)   #explore related_name
    prob_description = models.TextField()
    prob_file = models.ImageField(upload_to=f"{quiz.course.name}/quizzes")
    #how to take mcqs?

class Answer(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=CASCADE)
    ques = models.ForeignKey(Question,on_delete=CASCADE)
    solution_text = models.TextField()
    solutionFile = models.FileField(upload_to=f"{quiz.course.name}/quiz_answers")