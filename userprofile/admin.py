from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Course)
admin.site.register(models.CourseUserRelation)
admin.site.register(models.Lecture)
admin.site.register(models.LectureNotes)
admin.site.register(models.Assignments)
admin.site.register(models.Solutions)
admin.site.register(models.Solutionfeedback)
admin.site.register(models.Quiz)
admin.site.register(models.Question)
admin.site.register(models.Answer)