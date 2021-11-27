from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.forms import fields
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User

from userprofile.models import CsvFeedback

class CourseCreationForm(forms.Form):
    Course_name = forms.CharField(max_length=50)    #/dhvanit
    Course_code = forms.CharField(max_length=10)
    regcode_student = forms.CharField(max_length=10, label="Registration code (students)")
    regcode_TA = forms.CharField(max_length=10, label="Registration code (TAs)")
    email_invites = forms.BooleanField(required=False,initial=False, label='Send email invitations to all users?')

class CourseRegistrationForm(forms.Form):
    Course_name = forms.CharField(max_length=50)
    Course_code = forms.CharField(max_length=10)
    Registration_code = forms.CharField(max_length=10)  #dhvanit

class SetTAPrivilegesForm(forms.Form):  #/dhvanit
    can_grade = forms.BooleanField(required=False,initial=True,label='Grading assignments')
    can_create_assignments = forms.BooleanField(required=False,initial=False,label='Creating assignments')
    can_create_lectures = forms.BooleanField(required=False,initial=False,label='Uploading Lectures')

class ForumQuestionForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":50, 'placeholder':'Ask a question'}),label="")

class ForumAnswerForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":50, 'placeholder':'Write a reply'}),label="")

class DirectMessageForm(forms.Form): 
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":50, 'placeholder':'Write a message'}),label="")   #dhvanit/

class LectureCreationForm(forms.Form):
    title = forms.CharField(max_length=150)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":100, 'placeholder':'--Enter description here--'}),label="")
    notes = forms.FileField()

class AssignmentCreationForm(forms.Form):
    p_description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":70, 'placeholder':'Problem description'}),label="")
    Problem = forms.FileField()
    Deadline = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))

class SolutionSubmissionForm(forms.Form):
    solutionfile = forms.FileField(label='Submission')
    #sol_description = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":50, 'placeholder':'Solution Description'}),label="",required=False)

class SolutionFeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":50, 'placeholder':'Feedback'}),label="")

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100,widget=PasswordInput(attrs={'class':'form_control','type':'password'}))
    new_password1 = forms.CharField(max_length=100,widget=PasswordInput(attrs={'class':'form_control','type':'password'}))
    new_password2 = forms.CharField(max_length=100,widget=PasswordInput(attrs={'class':'form_control','type':'password'}))

    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')

class ChangeUserProfileForm(UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class CsvFeedbackSubmissionForm(forms.ModelForm):
    class Meta:
        model = CsvFeedback
        fields = ('feedback_csv',)
        labels = {'feedback_csv':'Upload Feedback in CSV File'}