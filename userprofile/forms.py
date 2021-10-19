from django import forms

class CourseCreationForm(forms.Form):
    name = forms.CharField(max_length=50)
    color = forms.CharField(max_length=7,initial='#007bff')
    code = forms.CharField(max_length=10)

class CourseRegistrationForm(forms.Form):
    Course_name = forms.CharField(max_length=50)
    Course_code = forms.CharField(max_length=10)

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